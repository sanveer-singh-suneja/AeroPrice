import sys
import numpy as np
import pandas as pd
import joblib
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import preprocess_input
from PIL import Image
import os

# ----------- CONFIG -----------
CSV_PATH = "data/austin_master_dataset.csv"
MODEL_PATH = "models/final_model_satellite.h5"  # multimodal trained on log(price)
SCALER_PATH = "models/num_scaler.pkl"
IMAGE_SIZE = (128, 128)
NUMERIC_COLS = ['livingAreaSqFt', 'yearBuilt', 'numOfBedrooms',
                'numOfBathrooms', 'avgSchoolRating', 'lotSizeSqFt']
# ------------------------------

def main():
    if len(sys.argv) < 3:
        print("Usage: python predict_cmd.py <row_index> <image_path>")
        sys.exit(1)
    try:
        idx = int(sys.argv[1])
    except Exception:
        print("First argument must be an integer row index")
        sys.exit(1)
    img_path_cli = sys.argv[2]

    # Load data
    df = pd.read_csv(CSV_PATH)
    if idx < 0 or idx >= len(df):
        print(f"Index {idx} out of range (dataset has {len(df)} rows).")
        sys.exit(1)

    row = df.iloc[idx]
    rgb_path = img_path_cli if img_path_cli else row.get('rgb_path')
    if not (isinstance(rgb_path, str) and os.path.exists(rgb_path)):
        print(f"Image path not found: {rgb_path}")
        sys.exit(1)

    # Load resources
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
    except Exception as e:
        print(f"Failed to load model at {MODEL_PATH}: {e}")
        sys.exit(1)
    scaler = joblib.load(SCALER_PATH)

    # --- Numeric input ---
    try:
        x_num = np.array([[row[c] for c in NUMERIC_COLS]], dtype='float32')
    except KeyError as e:
        print(f"Missing numeric column in CSV: {e}")
        sys.exit(1)
    x_num_scaled = scaler.transform(x_num)

    # --- Image input ---
    img = Image.open(rgb_path).convert('RGB').resize(IMAGE_SIZE)
    img_array = np.array(img).astype('float32')
    img_array = preprocess_input(img_array)
    x_img = np.expand_dims(img_array, axis=0)

    # --- Prediction (model outputs log(price)) ---
    pred_log = float(model.predict([x_img, x_num_scaled], verbose=0).reshape(-1)[0])
    pred_price = float(np.expm1(pred_log))

    # --- Print results ---
    actual_price = row.get('latestPrice', None)
    print(f"\n=== Multimodal Prediction for index {idx} ===")
    print(f"Using image: {rgb_path}")
    print(f"Predicted log(price): {pred_log:.4f}")
    print(f"Predicted price: ₹{pred_price:,.2f}")
    if actual_price is not None and not pd.isna(actual_price):
        print(f"Actual price:    ₹{float(actual_price):,.2f}")
        error = pred_price - float(actual_price)
        print(f"Error: ₹{error:+,.2f}")
    else:
        print("Actual price: (not available)")
    print("=================================\n")

if __name__ == "__main__":
    main()
