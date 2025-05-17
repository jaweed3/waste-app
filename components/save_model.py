import tensorflow as tf
import os

# Load the existiong Keras Model
model = tf.keras.models.load_model('./MobileNetV2Waste_Tuned.keras')

# Save in Tensorflow saved model format
export_path = './saved_model/1'
model.export(export_path, format='tf_saved_model')

print(f"Model Saved to {export_path}")