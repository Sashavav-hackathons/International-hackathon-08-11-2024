from flask import Flask
from flask_cors import CORS # Импортируем CORS
from requester import request_blueprint


def load_file_setup():
    UPLOAD_FOLDER = '../../TEST_DATA'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def create_app():
    app = Flask(__name__)
    app.register_blueprint(request_blueprint)
    
    CORS(app)

    return app

app = create_app()
load_file_setup()

if __name__ == '__main__':
    app.run(port=5000)
