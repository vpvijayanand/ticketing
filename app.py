from flask import Flask, request, jsonify
import tensorflow as tf
import pickle
import mariadb

# Load the models
category_model = tf.keras.models.load_model('models/category_model.h5')
severity_model = tf.keras.models.load_model('models/severity_model.h5')

# Load the vectorizer
with open('preprocessing/vectorizer.pkl', 'rb') as f:
    tfidf = pickle.load(f)

# Connect to MariaDB
conn = mariadb.connect(
    user="ticketadmin",
    password="Ticket@123",
    host="localhost",
    database="ticket_db"
)
cursor = conn.cursor()

# Flask app
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    problem_description = data.get('Problem_Description')

    # Vectorize the problem description
    problem_vec = tfidf.transform([problem_description]).toarray()

    # Predict category and severity
    category_pred = category_model.predict(problem_vec)
    severity_pred = severity_model.predict(problem_vec)

    category = category_pred.argmax()
    severity = severity_pred.argmax()

    # Find similar issues in the database
    cursor.execute("SELECT * FROM tickets WHERE Problem_Description LIKE ?", ('%' + problem_description + '%',))
    similar_issues = cursor.fetchall()

    return jsonify({
        'Category': int(category),
        'Severity': int(severity),
        'Similar Issues': similar_issues
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
