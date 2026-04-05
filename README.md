# AeroPrice 🛰️
### Multimodal Satellite Property Valuation System

> *Traditional real estate models look at zip codes and square footage.*  
> *They miss the neighborhood context—the greenery, the roof condition, the density.*  
> *AeroPrice sees the whole picture.*

**Team IRIS**

| Member | Role |
|---|---|
| Disha Goyal           | Backend API, Data Pipeline, Core ML Integration |
| Ramneek Kaur Dhillon  | Frontend UI, Streamlit Dashboard |
| Sanveer Singh         | Satellite Image Processing, ETL Pipeline |
| Jaspreet Singh        | Model Architecture & Training |
| Simarbir Singh Sandhu | Data Collection & Validation |
| Hitanshi Antil        | Deployment & Documentation |


---

## What is AeroPrice?

AeroPrice is a state-of-the-art multimodal machine learning application that predicts real estate prices in Austin, Texas. It doesn't just read tabular data—it actively parses geographic and environmental context using high-resolution Sentinel-2 satellite imagery.

By combining standard property features with raw pixel data and NDVI (vegetation index) maps, the model captures nuance that simple numeric models miss. 

**How it's different from generic ML models:**  
Most property price predictors use XGBoost on tabular data. AeroPrice merges two worlds. A standard neural network processes the numeric data (bedrooms, bathrooms, lot size), while a ResNet50 convolutional neural network extracts features from RGB satellite image patches. Both feature vectors are concatenated and passed through dense layers to output a highly accurate price prediction.

---

## Features

- **Multimodal Engine** — Combines tabular real estate data with raw satellite imagery.
- **Automated Data Pipeline** — Cleans data, computes geographic bounding boxes, and generates uniform 256x256 image patches.
- **NDVI Processing** — Extracts Normalized Difference Vegetation Index from satellite data to factor greenery into valuations.
- **ResNet50 Feature Extraction** — Uses transfer learning to understand structural contexts of neighborhoods from space.
- **Interactive Dashboard** — Streamlit frontend for users to easily interface with the model visually.
- **Robust API Backend** — Flask serves predictions seamlessly to the frontend.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Image Modeling | TensorFlow / Keras (ResNet50) |
| Tabular Modeling | TensorFlow Dense Networks |
| Data Processing | Pandas, Numpy, Scikit-Learn |
| Geospatial Processing | Rasterio |
| Backend API | Flask |
| Frontend UI | Streamlit |
| Explanations | SHAP (SHapley Additive exPlanations) |
| Image Manipulation | Pillow (PIL) |

---

## Repo Structure

```text
aeroprice/
│
├── data/                        # Processed Datasets & Media
│   ├── austin_master_dataset.csv
│   ├── austin_properties_cleaned.csv
│   ├── image_patches/           # 256x256 satellite crops
│   └── outputs/                 # Raw Sentinel-2 tif/png
│
├── models/                      # Saved Models & Weights
│   ├── final_model_satellite.h5 # Trained multimodal Keras model
│   └── num_scaler.pkl           # StandardScaler for tabular data
│
├── pipeline/                    # AI & Data Pipelines
│   ├── clean_austin_data.py
│   ├── compute_bbox_from_cleaned.py
│   ├── download_sentinel.py
│   ├── compute_ndvi.py
│   ├── generate_image_patches.py
│   ├── tf_pipeline_from_master.py
│   ├── model_def.py
│   ├── train_model.py
│   └── predict_cmd.py
│
├── backend/                     # API Server
│   └── main.py                  # Flask endpoints & model serving
│
├── frontend/                    # Web Interface
│   ├── app.py                   # Streamlit dashboard
│   └── public/                  # HTML/CSS/JS assets
│
├── main.py                      # Root launcher script
├── requirements.txt
└── README.md
```

---

## Data Flow

```text
Raw CSV → Cleaned CSV → Bounding Boxes → Sentinel-2 Download
                                               ↓
                                           NDVI Compute
                                               ↓
                              Image Patches (256x256) + Master CSV
                                               ↓
                      tf.data Pipeline → ResNet50 + Dense Model Training
                                               ↓
                                   Saved Model (.h5) + Scaler
                                               ↓
                         Flask API Backend  ←→  Streamlit Frontend
```

---

## Multimodal Fusion Logic

**Layer 1 — Image Processing:**
Sentinel-2 RGB images are passed through a pre-trained ResNet50 model (with frozen base layers). This acts as a spatial feature extractor, producing a dense lower-dimensional representation of the property's surroundings.

**Layer 2 — Tabular Feature Scaling:**
Traditional inputs (`livingAreaSqFt`, `yearBuilt`, `numOfBedrooms`, etc.) are transformed scaling using `num_scaler.pkl` to normalize variance.

**Fusion Layer:**
The outputs of Layer 1 and Layer 2 are concatenated. This global feature vector is funneled through fully connected dense layers with dropout for regularization. The final output is `log(price)`, which is exponentially transformed back to a predicted dollar value.

---

## Setup

### Prerequisites
- Python 3.8+
- Virtual environment recommended

### 1. Download Large Files
Due to GitHub file size limits, the trained model and image patches must be downloaded separately:
1. **Model Weights:** Download `final_model_satellite.h5` from [Hugging Face](https://huggingface.co/sanveer-singh/austin-property-predictor) and place it in the `models/` directory.
2. **Datasets:** Download the datasets and the `image_patches/` folder from [Kaggle](https://www.kaggle.com/datasets/sanveersinghsuneja/austin-satellite-property-data) and place them in the `data/` directory.

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
Use the master bootstrap script to start everything automatically:
```bash
python main.py
```

- Backend API runs at `http://localhost:5000`
- Streamlit UI runs at `http://localhost:8501`

*(Alternatively, you can run `predict_cmd.py` inside the `pipeline/` folder to test predictions directly via the terminal).*
