import pickle
from flask import Flask, request, render_template, jsonify
#all old code below: 
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
app = Flask(__name__, static_url_path="")

@app.route('/') 
def index():
    """Return the main page."""
    return render_template('doppel.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Return a character image."""
    data = request.json
    extraction = ImageFeatureExtractor()
    features_for_web = extraction.transform([data['user_input']])
    prediction = model.predict(features_for_web)
    return jsonify({'prediction': prediction[0]})

