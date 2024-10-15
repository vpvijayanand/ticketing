from flask import Flask, request, jsonify
import tensorflow as tf
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from google.cloud import translate_v2 as translate
from google.cloud import language_v1

app = Flask(__name__)

# Initialize Google Cloud clients
translate_client = translate.Client()
nlp_client = language_v1.LanguageServiceClient()

# Load the trained model and label encoders
model = tf.keras.models.load_model('model/ticket_classifier.keras')

with open('model/category_label_encoder.pkl', 'rb') as f:
    label_encoder_category = pickle.load(f)

with open('model/severity_label_encoder.pkl', 'rb') as f:
    label_encoder_severity = pickle.load(f)

# Load the TF-IDF vectorizer
df = pd.read_csv('data/payment_tickets_500.csv')
X = df['Problem Description']
tfidf = TfidfVectorizer(max_features=500)
tfidf.fit(X)

# Function to detect language and translate to English if necessary
def detect_and_translate_text(text):
    result = translate_client.detect_language(text)
    detected_language = result['language']

    if detected_language != 'en':
        translation = translate_client.translate(text, target_language='en')
        translated_text = translation['translatedText']
        return translated_text, detected_language
    else:
        return text, 'en'  # No translation needed, return the original text

# Function to analyze sentiment using Google Cloud NLP
def analyze_ticket_sentiment(ticket_text):
    document = language_v1.Document(content=ticket_text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = nlp_client.analyze_sentiment(request={'document': document}).document_sentiment
    return sentiment.score, sentiment.magnitude

# Function to classify ticket and prioritize based on sentiment
def triage_support_ticket(ticket_text):
    # Analyze sentiment of the ticket
    sentiment_score, sentiment_magnitude = analyze_ticket_sentiment(ticket_text)
    
    # Determine priority based on sentiment
    if sentiment_score < -0.5:
        priority = "High"
    elif sentiment_score < 0:
        priority = "Medium"
    else:
        priority = "Low"

    return {
        "Sentiment Score": sentiment_score,
        "Sentiment Magnitude": sentiment_magnitude,
        "Priority": priority
    }

# Route to handle POST requests for predictions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the problem description from the request
        data = request.json
        problem_description = data['problem_description']

        # Step 1: Detect language and translate if needed
        translated_text, detected_language = detect_and_translate_text(problem_description)

        # Step 2: Preprocess the input using the same TF-IDF vectorizer
        problem_tfidf = tfidf.transform([translated_text]).toarray()

        # Step 3: Use the model to make predictions
        predictions = model.predict(problem_tfidf)
        
        # Step 4: Decode the predictions
        predicted_category = np.argmax(predictions['category_output'], axis=1)
        predicted_severity = np.argmax(predictions['severity_output'], axis=1)

        category_label = label_encoder_category.inverse_transform(predicted_category)[0]
        severity_label = label_encoder_severity.inverse_transform(predicted_severity)[0]

        # Step 5: Analyze sentiment and triage the ticket
        sentiment_data = triage_support_ticket(translated_text)

        # Return the predictions in JSON format, along with the detected language and sentiment
        return jsonify({
            'original_language': detected_language,
            'translated_text': translated_text,
            'category': category_label,
            'severity': severity_label,
            'sentiment_score': sentiment_data['Sentiment Score'],
            'sentiment_magnitude': sentiment_data['Sentiment Magnitude'],
            'priority': sentiment_data['Priority'],
            'solution': 'Suggested solution will depend on the category and severity.'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Run the Flask app on port 80
    app.run(host='0.0.0.0', port=443)
