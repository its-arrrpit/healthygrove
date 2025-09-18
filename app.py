from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
# TensorFlow and related imports are temporarily commented out to focus on frontend
# import tensorflow as tf
# from PIL import Image
import numpy as np
import io

# Initialize the Flask application
app = Flask(__name__, static_folder='static')
CORS(app)  # This is to allow cross-origin requests from your frontend

# Serve the frontend
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# Serve static files (if you have JS/CSS/images in a static folder)
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)
CORS(app)  # This is to allow cross-origin requests from your frontend

# For the demo version, we'll use this list of class names without loading the model
# The full list is commented out and replaced with a limited list that matches the frontend database
# class_names = [
#     'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
#     'Corn_(maize)___Common_rust_',
#     'Corn_(maize)___Northern_Leaf_Blight',
#     'Corn_(maize)___healthy',
#     'Potato___Early_blight',
#     'Potato___Late_blight',
#     'Potato___healthy',
#     'Tomato___Bacterial_spot',
#     'Tomato___Early_blight',
#     'Tomato___Late_blight',
#     'Tomato___Leaf_Mold',
#     'Tomato___Septoria_leaf_spot',
#     'Tomato___Spider_mites Two-spotted_spider_mite',
#     'Tomato___Target_Spot',
#     'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
#     'Tomato___Tomato_mosaic_virus',
#     'Tomato___healthy'
# ]

# Limited list that matches the frontend database
class_names = [
    'Corn_(maize)___Common_rust_',
    'Potato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold'
]

# Print a message to indicate we're running in demo mode
print("Running in DEMO mode without TensorFlow. The model will return random predictions.")
model = None  # We'll simulate predictions instead

import random

def preprocess_image(image_bytes):
    """
    In demo mode, this function just returns True to indicate that an image was received
    """
    try:
        # Just checking if we have image data, not actually processing it
        if image_bytes:
            return True
        return None
    except Exception as e:
        print(f"Error with image: {e}")
        return None

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    # Get crop name if provided
    crop_name = request.form.get('crop_name', '')
    print(f"Received crop name: {crop_name}")

    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    if file:
        try:
            image_bytes = file.read()
            # In demo mode, just check if we got image data
            if preprocess_image(image_bytes) is None:
                return jsonify({'error': 'Could not process the image.'}), 400

            # If a crop name was provided, use it to filter the possible diseases
            filtered_classes = class_names
            if crop_name:
                filtered_classes = [name for name in class_names if name.lower().startswith(crop_name.lower())]
                if not filtered_classes:  # If no matching diseases found, fall back to all classes
                    filtered_classes = class_names
            
            # Pick a random class from filtered list
            predicted_class_name = random.choice(filtered_classes)
            
            # Generate a random confidence between 75% and 99%
            confidence = random.uniform(0.75, 0.99)

            # Return the result as JSON
            return jsonify({
                'disease': predicted_class_name,
                'confidence': f"{confidence:.2%}",
                'specified_crop': bool(crop_name)  # Indicate if user specified a crop
            })

        except Exception as e:
            print(f"Prediction Error: {e}")
            return jsonify({'error': 'An error occurred during prediction.'}), 500
    
    return jsonify({'error': 'An unknown error occurred.'}), 500


if __name__ == '__main__':
    # Runs the Flask server on localhost, port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
