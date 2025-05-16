import tensorflow as tf

# Load the existiong Keras Model
model = tf.keras.models.load_model('./MobileNetV2Waste_Tuned.keras')

# Save in Tensorflow saved model format
export_path = './waste_classifier/1'
model.export(model, export_path)

print(f"Model Saved to {export_path}")