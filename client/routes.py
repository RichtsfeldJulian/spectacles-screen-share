from flask import Blueprint, send_file

screen_routes = Blueprint('screen_routes', __name__)

def init_routes(screen_capture):
    
    @screen_routes.route('/screen.jpg')
    def get_screen():
        try:
            frame = screen_capture.get_current_frame()
            return send_file(frame, mimetype='image/jpeg')
        except Exception as e:
            print(f"Error serving frame: {e}")
            return send_file(
                screen_capture._create_blank_frame(), 
                mimetype='image/jpeg'
            )

    return screen_routes