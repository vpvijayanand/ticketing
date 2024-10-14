from flask import Flask, request, jsonify
import tensorflow as tf
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

app = Flask(__name__)

# Load the trained model and label encoders
model = tf.keras.models.load_model('model/ticket_classifier.keras')

with open('model/category_label_encoder.pkl', 'rb') as f:
    label_encoder_category = pickle.load(f)

with open('model/severity_label_encoder.pkl', 'rb') as f:
    label_encoder_severity = pickle.load(f)

# Load the TF-IDF vectorizer (you may need to retrain it if it's not saved)
df = pd.read_csv('data/payment_tickets_500.csv')
X = df['Problem Description']
tfidf = TfidfVectorizer(max_features=500)
tfidf.fit(X)

# Route to handle POST requests for predictions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the problem description from the request
        data = request.json
        problem_description = data['problem_description']

        # Step 1: Preprocess the input using the same TF-IDF vectorizer
        problem_tfidf = tfidf.transform([problem_description]).toarray()

        # Step 2: Use the model to make predictions
        predictions = model.predict(problem_tfidf)
        
        # Step 3: Decode the predictions
        predicted_category = np.argmax(predictions['category_output'], axis=1)
        predicted_severity = np.argmax(predictions['severity_output'], axis=1)

        category_label = label_encoder_category.inverse_transform(predicted_category)[0]
        severity_label = label_encoder_severity.inverse_transform(predicted_severity)[0]

        # Return the predictions in JSON format
        return jsonify({
            'category': category_label,
            'severity': severity_label,
            'solution': 'Suggested solution will depend on the category and severity.'  # You can customize this logic
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Run the Flask app on port 80
    app.run(host='0.0.0.0', port=80)
