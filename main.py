
import os
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    import eventlet
    eventlet.monkey_patch(os=False)
    logger.info("Eventlet monkey patching completed")
except Exception as e:
    logger.error(f"Failed to initialize eventlet: {str(e)}")
    raise

try:
    from app import app, socketio

    if __name__ == "__main__":
        port = int(os.environ.get('PORT', 5000))
        logger.info(f"Starting Flask server on port {port}...")
        socketio.run(
            app,
            host='0.0.0.0',
            port=port,
            debug=True,
            use_reloader=False,
            log_output=True
        )
except Exception as e:
    logger.error(f"Failed to start Flask server: {str(e)}", exc_info=True)
    raise
