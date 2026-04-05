# 🛰️ AeroPrice - AI-Powered Satellite Property Valuation

**Revolutionary property valuation using satellite imagery and machine learning**

## 🌟 Features

### 🎯 Core Capabilities
- **Satellite Image Analysis**: Uses TensorFlow/ResNet50 to analyze property satellite imagery
- **AI Price Prediction**: Multimodal model combining visual and tabular data
- **Human-Readable Explanations**: Natural language generation for prediction insights
- **Amenity Inference**: Smart deduction of nearby amenities from visual features
- **Interactive Visualizations**: Real-time charts and plots for explainability

### 🖥️ Multiple Interfaces
- **Streamlit Dashboard**: Modern, interactive web interface
- **Flask API**: RESTful backend for integration
- **HTML Frontend**: Clean, responsive web interface
- **CLI Tools**: Command-line prediction utilities

### 📊 Explainability Features
- **Feature Contributions**: See how each factor affects price
- **SHAP Analysis**: Advanced model interpretability
- **Score Breakdowns**: Neighborhood, accessibility, and green space ratings
- **Visual Charts**: Interactive plots for data exploration

## 🚀 Quick Start

### Option 1: One-Click Launch (Recommended)
```bash
python start_aeroprice.py
```
This script will:
- Check all dependencies
- Start the Flask backend
- Launch the Streamlit interface
- Open your browser automatically

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Start Flask backend
python backend_app.py

# In another terminal, start Streamlit
streamlit run aeroprice_streamlit.py
```

## 📁 Project Structure

```
Hackathon -1/
├── 🛰️ Core System
│   ├── backend_app.py              # Flask API with enhanced features
│   ├── aeroprice_streamlit.py      # Modern Streamlit dashboard
│   ├── start_aeroprice.py          # One-click startup script
│   └── index.html                  # Basic HTML interface
│
├── 🤖 Machine Learning
│   ├── final_model.h5              # Trained multimodal model
│   ├── model_def.py                # Model architecture
│   ├── train_model.py              # Training script
│   ├── tf_pipeline_from_master.py  # Data pipeline
│   └── num_scaler.pkl              # Feature scaler
│
├── 📊 Data & Assets
│   ├── austin_master_dataset.csv   # Property dataset
│   ├── image_patches/              # Satellite image patches
│   └── static/plots/               # Generated charts
│
├── 🛠️ Utilities
│   ├── predict_cmd.py              # CLI prediction tool
│   ├── clean_austin_data.py        # Data preprocessing
│   └── generate_image_patches.py   # Image processing
│
└── 📋 Documentation
    ├── README_AEROPRICE.md         # This file
    └── requirements.txt            # Python dependencies
```

## 🔧 API Endpoints

### Core Prediction
- `POST /predict` - Predict property price with satellite image
- `GET /properties` - Get list of available properties
- `POST /explain_prediction` - Get detailed explanation with charts

### Enhanced Features
- `POST /explain_multimodal` - SHAP explainability for images
- Static chart serving from `/static/plots/`

## 💡 Usage Examples

### Streamlit Interface
1. Run `streamlit run aeroprice_streamlit.py`
2. Select a property from the dropdown
3. Click "Analyze Property" to get prediction
4. View satellite image and scores
5. Click "Get Detailed Explanation" for full analysis

### Flask API
```python
import requests

# Get property prediction
response = requests.post('http://localhost:5000/predict', 
                        json={'property_index': 123})
data = response.json()

print(f"Predicted Price: ${data['predicted_price']:,.0f}")
print(f"Neighborhood Score: {data['neighborhood_score']}/10")
```

### CLI Prediction
```bash
python predict_cmd.py 123 image_patches/property_123_rgb.png
```

## 🎨 Interface Options

### 1. Streamlit Dashboard (Recommended)
- **Modern UI**: Beautiful, responsive design
- **Interactive Charts**: Plotly visualizations
- **Real-time Analysis**: Live prediction updates
- **Satellite Images**: Direct image display
- **Access**: http://localhost:8501

### 2. HTML Frontend
- **Classic Web**: Traditional web interface
- **Dark Theme**: Space-inspired design
- **Mobile Responsive**: Works on all devices
- **Access**: Open `index.html` in browser

### 3. Flask API
- **Developer Friendly**: RESTful endpoints
- **Integration Ready**: Easy to embed
- **JSON Responses**: Structured data
- **Access**: http://localhost:5000

## 🧠 AI Features

### Explanation Generator
- **Natural Language**: Human-readable insights
- **Context Aware**: Adapts to price ranges
- **Factor Analysis**: Identifies key drivers

### Feature Inference Engine
- **Amenity Detection**: Infers nearby facilities
- **Confidence Levels**: High/moderate/low confidence
- **Reasoning**: Explains inference logic

### Chart Generation
- **Feature Contributions**: Bar charts showing impact
- **Predicted vs Actual**: Scatter plots
- **SHAP Analysis**: Advanced explainability
- **Model Metrics**: Performance visualization

## 📊 Sample Output

### Prediction Response
```json
{
  "predicted_price": 485000.00,
  "actual_price": 480000.00,
  "neighborhood_score": 8.5,
  "accessibility_score": 7.2,
  "green_space_score": 6.8,
  "satellite_image": "data:image/png;base64,...",
  "image_metadata": {
    "location": "123 Main St, Austin, TX 78701",
    "capture_date": "2020",
    "resolution": "10m"
  }
}
```

### Explanation Response
```json
{
  "summary_text": "📍 Property Analysis Complete\n\n💰 Predicted Price: $485,000\n\n📝 Analysis Summary:\nThis property shows balanced characteristics with extensive green spaces and excellent accessibility, though some limitations from developing neighborhood infrastructure.\n\n🏫 Inferred Amenities:\nBased on the area characteristics, Schools are possibly within 2-3 km, Healthcare are likely within 5-6 km.",
  "contributions": {
    "neighborhood": 52500.0,
    "accessibility": 26400.0,
    "green_space": 32400.0
  },
  "inferred_amenities": {
    "schools": {
      "proximity": "possibly within 2-3 km",
      "confidence": "moderate"
    }
  },
  "charts": [...]
}
```

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV=development` - Enable debug mode
- `PORT=5000` - Flask port
- `STREAMLIT_PORT=8501` - Streamlit port

### Model Configuration
- **Image Size**: 128x128 pixels
- **Preprocessing**: ResNet50 preprocessing
- **Features**: 6 numerical features
- **Architecture**: Multimodal (image + tabular)

## 🐛 Troubleshooting

### Common Issues

1. **Model Not Found**
   ```
   Solution: Ensure final_model.h5 is in the project directory
   ```

2. **Images Not Loading**
   ```
   Solution: Check image_patches/ directory and rgb_path in CSV
   ```

3. **Streamlit Won't Start**
   ```
   Solution: pip install streamlit requests plotly
   ```

4. **Charts Not Displaying**
   ```
   Solution: Check static/plots/ directory permissions
   ```

### Performance Tips
- Use GPU if available for faster predictions
- Clear old chart files periodically
- Monitor memory usage with large datasets

## 🏆 Hackathon Features

### Demo-Ready Components
- **Live Satellite Images**: Real property imagery
- **Interactive Charts**: Engaging visualizations
- **Smart Explanations**: AI-generated insights
- **Multiple Interfaces**: Flexible presentation options

### Presentation Tips
- Start with Streamlit interface for best visuals
- Show satellite image analysis in action
- Demonstrate explanation features
- Highlight amenity inference capabilities

## 📈 Future Enhancements

### Planned Features
- **Real-time Map Integration**: Interactive property selection
- **Batch Processing**: Multiple property analysis
- **Export Functionality**: PDF reports
- **Mobile App**: Native mobile interface
- **Advanced Analytics**: Market trend analysis

### Technical Improvements
- **GPU Acceleration**: Faster model inference
- **Caching System**: Redis for performance
- **Async Processing**: Celery for heavy tasks
- **API Rate Limiting**: Production-ready scaling

## 🤝 Contributing

### Development Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `python -m pytest tests/`
4. Start development server: `python start_aeroprice.py`

### Code Style
- Follow PEP 8 guidelines
- Use type hints where possible
- Document functions with docstrings
- Add error handling for robustness

## 📄 License

This project is developed for hackathon demonstration purposes.

## 🙏 Acknowledgments

- **TensorFlow Team**: For the deep learning framework
- **Streamlit**: For the beautiful web interface
- **Austin Open Data**: For the property dataset
- **Sentinel Hub**: For satellite imagery data

---

**🛰️ AeroPrice - Where AI meets real estate through satellite vision!**
