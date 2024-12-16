import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import MeanSquaredError as mse_metric
from tensorflow.keras.utils import get_custom_objects
from minio import Minio
import joblib
import os
from sklearn.metrics import mean_squared_error
from keras.saving import register_keras_serializable

@register_keras_serializable()
def mse(y_true, y_pred):
    return MeanSquaredError()(y_true, y_pred)

get_custom_objects().update({"mse": mse})

MINIO_CLIENT = Minio(
    "localhost:9000",
    access_key="minio",
    secret_key="minio123",
    secure=False
)
MODEL_BUCKET = "product-model"
MODEL_NAME = "product_lstm_model.h5"
SCALER_NAME = "scaler.gz"

MODEL = None
SCALER = None

def load_model_and_scaler():
    global MODEL, SCALER

    if MODEL is None or SCALER is None:
        model_path = "temp_model.h5"
        MINIO_CLIENT.fget_object(MODEL_BUCKET, MODEL_NAME, model_path)
        MODEL = load_model(model_path, custom_objects={"mse": mse})
        os.remove(model_path)

        scaler_path = "temp_scaler.gz"
        MINIO_CLIENT.fget_object(MODEL_BUCKET, SCALER_NAME, scaler_path)
        SCALER = joblib.load(scaler_path)
        os.remove(scaler_path)

    return MODEL, SCALER

def get_predictions(input_data):
    model, scaler = load_model_and_scaler()

    input_data = np.array(input_data).reshape(-1, 1)
    input_data_scaled = scaler.transform(input_data)
    sequence_length = 5

    X = input_data_scaled[-sequence_length:].reshape(1, sequence_length, 1)

    predictions = []
    for _ in range(5):
        pred = model.predict(X, verbose=0)
        predictions.append(pred[0][0])

        new_input = np.array([[pred[0][0]]])
        X = np.append(X[:, 1:, :], new_input.reshape(1, 1, 1), axis=1)

    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()
    return predictions

def evaluate_predictions(actuals, predictions):
    return np.sqrt(mean_squared_error(actuals, predictions))