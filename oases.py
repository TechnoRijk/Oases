#oases.py
from flask import Flask
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager
from extensions import db, login_manager
from api import api_blueprint
from flask_uploads import configure_uploads, IMAGES, UploadSet
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize the login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Database initialization
db.init_app(app)
migrate = Migrate(app, db)

# Flask-Uploads setup
images = UploadSet('images', IMAGES)
app.config['UPLOADED_IMAGES_DEST'] = app.config.get('UPLOADED_IMAGES_DEST', 'static/images')
configure_uploads(app, images)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(api_blueprint, url_prefix='/api/v1')

import routes

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)