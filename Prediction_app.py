from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Load the trained model
try:
    model = joblib.load('random_forest_model.pkl')
except Exception as e:
    raise Exception(f"Model not found: {e}")

# Initialize Flask app
app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return "The API is working"

# Prediction route
@app.route("/predict", methods=['POST'])
def predict():
    try:
        data = request.json  # Get JSON data from request
        input_data = pd.DataFrame([data])

        # Define required features
        features = ['Protein intake (g/kg/day)', 'Energy intake (kcal/kg/day)', 'BMI (kg/m2)', 'Age (years)', 'Duration (weeks)', '(times/week)', 'Weight (kg)']

        # Validate input features
        if not all(feature in input_data.columns for feature in features):
            return jsonify({'error': "Missing required features"}), 400

        # Ensure the input data has the correct features
        input_data = input_data[features]

        # Make prediction
        prediction = model.predict(input_data)[0]

        # Calculate weeks required (assuming 0.5 kg/week)
        weeks_required = abs(prediction) / 0.5

        # Return prediction and weeks required
        return jsonify({
            'LBM Change Prediction (kg)': prediction,
            'Weeks Required': round(weeks_required, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)  # Enable debug mode for troubleshooting