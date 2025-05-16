import tempfile
import os
import tensorflow as tf

def export_model():
    model = tf.keras.models.load_model('MobileNetV2Waste_Tuned.keras')
    MODEL_DIR = tempfile.gettempdir()
    version = 1.0
    export_path = os.path.join(MODEL_DIR, str(version + 0.1))
    print('export_path = {}\n'.format(export_path))

    model.export(filepath = export_path)