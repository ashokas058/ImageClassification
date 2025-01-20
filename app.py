from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import base64
import os
import tensorflow as tf


app = Flask(__name__)
CORS(app)


gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)

MODEL_PATH = 'models/imageclassifier.h5'
model = load_model(MODEL_PATH)

def preprocess_image(frame):
    """Preprocess a video frame for the model."""
    # Resize the frame to the required input size (e.g., 224x224)
    resized_frame = cv2.resize(frame, (256, 256))
    # Normalize pixel values to [0, 1]
    img_array = img_to_array(resized_frame) / 255.0
    # Expand dimensions to add batch size
    return np.expand_dims(img_array, axis=0)

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests from the frontend."""
    try:
        # Get the frame from the request
        data = request.json
        frame_data = data['frame']
        # Decode the base64-encoded frame
        frame_bytes = base64.b64decode(frame_data.split(',')[1])
        print (str(frame_bytes))

        frame_array = np.frombuffer(frame_bytes, np.uint8)
        frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)

        # Preprocess the frame
        preprocessed_frame = preprocess_image(frame)

        # Make predictions
        prediction = model.predict(preprocessed_frame)
        label = int(np.argmax(prediction, axis=1)[0])  # Convert to integer (0 or 1)

        return jsonify({'label': label}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Ensure the app is available for remote access
    app.run(host='0.0.0.0', port=5000, debug=True)
