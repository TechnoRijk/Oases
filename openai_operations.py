# openai_operations.py

from flask import request, jsonify
import openai

def create_image():
    prompt = request.json.get('prompt')
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response.data[0]['url']  # Assuming response structure contains a URL
        return jsonify({"status": "success", "message": "Image created successfully", "image_url": image_url})
    except openai.Error as e:
        return jsonify({"error": str(e)}), 500
