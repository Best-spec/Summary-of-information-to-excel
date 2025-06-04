from flask import Flask
from flask_cors import CORS
from api.summary import summary_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(summary_bp)

    return app

if __name__ == '__main__':
    from config import PORT, DEBUG
    app = create_app()
    app.run(debug=DEBUG, port=PORT)
