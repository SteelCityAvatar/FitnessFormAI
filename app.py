import os
import logging
import tempfile

# Configure logging first
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    # Initialize computer vision components first
    import cv2
    import numpy as np
    import mediapipe as mp
    from utils.pose_analyzer import analyze_pose
    from utils.classifier import classify_form

    # Force CPU-only mode for MediaPipe
    os.environ['MEDIAPIPE_CPU_ONLY'] = '1'

    # Initialize MediaPipe Pose
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        enable_segmentation=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    logger.info("MediaPipe initialized successfully")

except ImportError as e:
    logger.error(f"Failed to import required packages: {str(e)}")
    raise
except Exception as e:
    logger.error(f"Failed to initialize MediaPipe: {str(e)}")
    raise

# Initialize eventlet after CV components
try:
    import eventlet
    eventlet.monkey_patch()
    logger.info("Eventlet initialized successfully")
except ImportError:
    logger.error("Eventlet required for WebSocket support")
    raise

# Flask imports after eventlet monkey patch
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY") or "squat_analyzer_secret"
app.config['DEBUG'] = True

# Initialize SocketIO with optimized configuration
socketio = SocketIO(
    app,
    async_mode='eventlet',
    logger=True,
    engineio_logger=True,
    cors_allowed_origins="*",
    ping_timeout=5000,
    ping_interval=25000,
    max_http_buffer_size=1e8
)

@app.route('/')
def index():
    """Serve the main page."""
    logger.debug("Serving index page")
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    logger.info(f"Client connected: {request.sid}")
    emit('connection_status', {'status': 'connected'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    logger.info(f"Client disconnected: {request.sid}")

@socketio.on('process_frame')
def handle_frame(frame_data):
    """Handle incoming frame from webcam."""
    try:
        # Convert frame data to numpy array
        nparr = np.frombuffer(frame_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            logger.error("Failed to decode frame data")
            emit('error', {'message': 'Failed to decode frame data'})
            return

        # Process frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if not results.pose_landmarks:
            logger.debug("No pose detected in frame")
            emit('error', {'message': 'No pose detected'})
            return

        # Extract landmarks and analyze
        landmarks = [[lm.x, lm.y, lm.z] for lm in results.pose_landmarks.landmark]
        pose_analysis = analyze_pose([landmarks])
        form_classification = classify_form(pose_analysis)

        # Send results back to client
        emit('pose_analysis', {
            'success': True,
            'analysis': pose_analysis,
            'classification': form_classification
        })

    except Exception as e:
        logger.error(f"Error processing frame: {str(e)}", exc_info=True)
        emit('error', {'message': str(e)})

@app.route('/analyze', methods=['POST'])
def analyze_video():
    """Analyze uploaded video for squat form."""
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400

        video_file = request.files['video']

        # Save uploaded video to temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        video_file.save(temp_file.name)
        logger.debug(f"Saved uploaded video to temporary file: {temp_file.name}")

        # Process video frames
        cap = cv2.VideoCapture(temp_file.name)
        frames_data = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(frame_rgb)

            if results.pose_landmarks:
                landmarks = [[lm.x, lm.y, lm.z] for lm in results.pose_landmarks.landmark]
                frames_data.append(landmarks)

        cap.release()
        os.unlink(temp_file.name)
        logger.debug(f"Processed {len(frames_data)} frames from video")

        if not frames_data:
            return jsonify({'error': 'No pose detected in video'}), 400

        # Analyze the sequence
        pose_analysis = analyze_pose(frames_data)
        form_classification = classify_form(pose_analysis)

        return jsonify({
            'success': True,
            'analysis': pose_analysis,
            'classification': form_classification
        })

    except Exception as e:
        logger.error(f"Error processing video: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    logger.info("Starting Flask-SocketIO server...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False, log_output=True)