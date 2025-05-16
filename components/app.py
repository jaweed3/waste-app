from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import os

IMG_SIZE = 224
app = Flask(__name__)

# Loading the model
try:
    model = tf.keras.models.load_model('/waste-app/MobileNetV2Waste_Tuned.keras')
    print("Model loaded successfully")
except Exception as e:
    print(f"Can't load the model: {e}")

# Defining preprocessing function
def preprocess_image(image_path):
    img = tf.keras.utils.load_img(
        image_path,
        target_size=(IMG_SIZE, IMG_SIZE),
        color_mode='rgb'
    )
    img_array = tf.keras.utils.img_to_array(
        img,
        dtype=tf.float32,
    )
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    img_array = tf.expand_dims(img_array, axis=0)
    img_array = tf.image.convert_image_dtype(img_array, dtype=tf.float32)
    img_array = tf.image.resize(img_array, (IMG_SIZE, IMG_SIZE))
    img_array = tf.cast(img_array, tf.float32)
    img_array = tf.image.per_image_standardization(img_array)
    img_array = tf.image.resize_with_crop_or_pad(img_array, IMG_SIZE, IMG_SIZE)
    return img_array

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    # Save the uploaded file temporarily
    temp_path = os.path.join('/tmp', image_file.filename)
    image_file.save(temp_path)
    
    try:
        # Preprocess the image
        img_array = preprocess_image(temp_path)
        
        # Make prediction
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)
        
        # Clean up
        os.remove(temp_path)
        
        return jsonify({
            'predicted_class': int(predicted_class[0]),
            'confidence': float(predictions[0][predicted_class[0]])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)