from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from producer import send_to_kafka
from inference import get_predictions
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from minio import Minio
import joblib
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# MinIO Configuration
MINIO_CLIENT = Minio(
    "localhost:9000",
    access_key="minio",
    secret_key="minio123",
    secure=False
)
BUCKET_NAME = "product-model"
MODEL_NAME = "product_lstm_model.h5"
SCALER_NAME = "scaler.gz"

# Flask Configuration
app = Flask(__name__, static_folder='../web')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('../web', 'index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        if not data or 'features' not in data:
            return jsonify({"error": "Invalid input, 'features' data is required"}), 400

        features = [float(value) for value in data['features']]

        if not features or any(value < 0 for value in features):
            return jsonify({"error": "Invalid 'features' data: must be non-negative numbers"}), 400

        send_to_kafka(features)

        predictions = get_predictions(features).tolist()
        response = {"predictions": predictions}
        train_model(features, predictions)

        return jsonify(response)
    except Exception as e:
        logging.error(f"Error during prediction: {str(e)}")
        return jsonify({"error": str(e)}), 500

def train(user_closes, previous_predictions):
    try:
        logging.info("Starting the training process...")

        if not MINIO_CLIENT.bucket_exists(BUCKET_NAME):
            MINIO_CLIENT.make_bucket(BUCKET_NAME)

        scaler = MinMaxScaler()
        combined_data = np.array(user_closes + previous_predictions).reshape(-1, 1)
        data_scaled = scaler.fit_transform(combined_data)

        sequence_length = 5
        X, y = [], []
        for i in range(len(data_scaled) - sequence_length):
            X.append(data_scaled[i:i + sequence_length])
            y.append(data_scaled[i + sequence_length])
        X = np.array(X).reshape(-1, sequence_length, 1)
        y = np.array(y)

        model = Sequential([
            LSTM(50, activation='relu', input_shape=(sequence_length, 1)),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        model.fit(X, y, epochs=20, batch_size=16, verbose=2)

        local_model_path = MODEL_NAME
        model.save(local_model_path)
        MINIO_CLIENT.fput_object(BUCKET_NAME, MODEL_NAME, local_model_path)

        local_scaler_path = SCALER_NAME
        joblib.dump(scaler, local_scaler_path)
        MINIO_CLIENT.fput_object(BUCKET_NAME, SCALER_NAME, local_scaler_path)

        os.remove(local_model_path)
        os.remove(local_scaler_path)

    except Exception as e:
        logging.error(f"Error during training: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True, port=5000)