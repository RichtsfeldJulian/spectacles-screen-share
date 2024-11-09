from flask import Flask
from screen_capture import ScreenCaptureManager
from routes import init_routes
from config import config
import os

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize screen capture
    screen_capture = ScreenCaptureManager(
        compression_quality=app.config['COMPRESSION_QUALITY'],
        scale_factor=app.config['SCALE_FACTOR']
    )
    
    # Register routes
    app.register_blueprint(init_routes(screen_capture))
    
    return app, screen_capture

def main():
    # Get environment from environment variable or use default
    env = os.getenv('FLASK_ENV', 'development')
    
    print(f"Starting server in {env} mode...")
    app, screen_capture = create_app(env)
    
    print("Starting screen capture thread...")
    screen_capture.start()
    
    print(f"Starting Flask server on {config[env].HOST}:{config[env].PORT}...")
    app.run(
        host=config[env].HOST,
        port=config[env].PORT,
        debug=config[env].DEBUG
    )

if __name__ == '__main__':
    main()