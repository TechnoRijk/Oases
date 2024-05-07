# image_processing.py

from flask import request, jsonify
from flask_uploads import UploadSet, configure_uploads, IMAGES

images = UploadSet('images', IMAGES)
# Configure image upload settings
# app.config['UPLOADED_IMAGES_DEST'] = 'path/to/your/uploaded/images'
# configure_uploads(app, images)

def upload_image():
    if 'image' not in request.files:
        return jsonify({'message': 'No image file provided'}), 400
    file = request.files['image']
    filename = images.save(file)
    return jsonify({'message': 'Image uploaded successfully', 'filename': filename})