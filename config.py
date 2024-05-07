#config.py
import os
import openai
from flask_uploads import configure_uploads, IMAGES, UploadSet
from dotenv import load_dotenv
import secrets
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'path_to_your_module_directory'))

def configure_app(app):
    secret_key = secrets.token_hex(16)
    print(secret_key)

    openai.api_key = os.getenv('OPENAI_API_KEY')
    if not openai.api_key:
        raise ValueError("API key is not set. Check your .env file.")


    load_dotenv()

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    print(os.urandom(24))

    app.config['UPLOADED_IMAGES_DEST'] = 'static/images'  # or your chosen path
    images = UploadSet('images', IMAGES)
    configure_uploads(app, images)

class Config:
    SECRET_KEY = os.environ.get(
        '\xda\xe1\x03\xb2t\xbaG\x19D4\xb4\x9a\xa0\xa0\n\xaa\xd2\x19\xea2\xe5\xba\x1f|') or 'a very hard to guess string'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'postgresql://technorijk:lenovo@localhost/Oases'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
