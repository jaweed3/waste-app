from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import requests
import json
import os
from PIL import Image
import io

app = Flask(__name__)

# Configuration
IMG_SIZE = 224
TF_SERVING_URL = "http://localhost:8501/v1/models/waste_classifier:predict"
CLASS_NAMES = ["Organic", "Recycleable", "Hazardous"] # Class Names

def preprocess_image(image_file):
    # Read image file
    img = Image.open(image_file)

    # Resice to expected dimensions
    img = img.resize((IMG_SIZE, IMG_SIZE))

    # Convert to numpy array
    img_array = tf.keras.utils.img_to_array(img)

    # Apply MobileNetV2 Preprocessing
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

    # Adding batch dimension
    img_array = np.expand_dims(img_array, axis=0)

    # Standardize
    img_array = tf.image.per_image_standardization(img_array).numpy()

    return img_array

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No Image file Provided'}), 400
    
    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No Image File Selected'}), 400
    
    try:
        # Preprocess the Image
        img_array = preprocess_image()

        # Prepare data for TF Serving
        data = json.dumps({
            "signature_name": "serving_default",
            "instances": img_array.tolist()
        })

        # Make request to TF serving
        headers = {'content-type': 'application/json'}
        tf_serving_response = requests.post(TF_SERVING_URL, data=data, headers=headers)

        if tf_serving_response.status_code != 200:
            return jsonify({'error': f'TF Serving Error: {tf_serving_response.text}'})
        
        predictions = tf_serving_response.json()['predictions'][0]
        predicted_class = np.argmax(predictions)
        confidence = float(predictions[predicted_class])

        return jsonify({
            'predicted_class': int(predicted_class),
            'class_name': CLASS_NAMES[predicted_class],
            'confidence': confidence
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/')
def index():
    return """
    <html>
        <body>
            <h1>Waste Classification API</h1>
            <p>Use the /predict endpoint with a POST request containing an image file.</p>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)