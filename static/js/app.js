document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('uploadForm');
    const videoInput = document.getElementById('videoInput');
    const videoPreview = document.getElementById('videoPreview');
    const processingIndicator = document.getElementById('processingIndicator');
    const results = document.getElementById('results');
    const formScore = document.getElementById('formScore');
    const feedback = document.getElementById('feedback');
    const liveModeBtn = document.getElementById('liveModeBtn');
    let isLiveMode = false;
    let socket;

    async function setupWebcam() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                video: { 
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                } 
            });
            videoPreview.srcObject = stream;
            videoPreview.classList.remove('d-none');
            return true;
        } catch (error) {
            console.error('Error accessing webcam:', error);
            alert('Unable to access webcam. Please check permissions.');
            return false;
        }
    }

    function startSocketConnection() {
        socket = io();

        socket.on('connect', function() {
            console.log('Socket connected');
        });

        socket.on('pose_analysis', function(data) {
            updateResults(data);
            updateCanvas(data.analysis);
        });

        socket.on('connect_error', function(error) {
            console.error('Socket connection error:', error);
            stopLiveMode();
        });
    }

    function stopLiveMode() {
        isLiveMode = false;
        if (videoPreview.srcObject) {
            videoPreview.srcObject.getTracks().forEach(track => track.stop());
        }
        if (socket) {
            socket.disconnect();
        }
        videoPreview.classList.add('d-none');
        liveModeBtn.innerHTML = '<i class="fas fa-camera"></i> Start Live Analysis';
        results.classList.add('d-none');
        form.classList.remove('d-none');
    }

    async function toggleLiveMode() {
        if (isLiveMode) {
            stopLiveMode();
        } else {
            form.classList.add('d-none');
            if (await setupWebcam()) {
                isLiveMode = true;
                liveModeBtn.innerHTML = '<i class="fas fa-stop"></i> Stop Live Analysis';
                startSocketConnection();
                startVideoProcessing();
            } else {
                form.classList.remove('d-none');
            }
        }
    }

    function startVideoProcessing() {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');

        function processFrame() {
            if (!isLiveMode) return;

            canvas.width = videoPreview.videoWidth;
            canvas.height = videoPreview.videoHeight;
            ctx.drawImage(videoPreview, 0, 0);

            canvas.toBlob(function(blob) {
                socket.emit('process_frame', blob);
            }, 'image/jpeg', 0.8);

            requestAnimationFrame(processFrame);
        }

        videoPreview.addEventListener('play', processFrame);
    }

    function updateResults(data) {
        results.classList.remove('d-none');
        formScore.className = 'alert';
        formScore.classList.add(data.classification.is_good ? 'alert-success' : 'alert-warning');
        formScore.textContent = `Form Score: ${Math.round(data.classification.confidence * 100)}%`;

        feedback.innerHTML = '';
        data.classification.feedback.forEach(item => {
            const li = document.createElement('div');
            li.className = 'list-group-item';
            li.textContent = item;
            feedback.appendChild(li);
        });
    }

    // Event Listeners
    liveModeBtn.addEventListener('click', toggleLiveMode);

    videoInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            videoPreview.src = URL.createObjectURL(file);
            videoPreview.classList.remove('d-none');
            results.classList.add('d-none');
        }
    });

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        if (isLiveMode) return;

        const file = videoInput.files[0];
        if (!file) {
            alert('Please select a video file');
            return;
        }

        processingIndicator.classList.remove('d-none');
        results.classList.add('d-none');

        const formData = new FormData();
        formData.append('video', file);

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            if (data.error) {
                throw new Error(data.error);
            }

            updateResults(data);
            updateCanvas(data.analysis);

        } catch (error) {
            alert(`Error: ${error.message}`);
        } finally {
            processingIndicator.classList.add('d-none');
        }
    });
});