import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import tensorflow as tf
import pickle

# Load the CSV data
df = pd.read_csv('data/ticket_data.csv')

# Vectorize the problem descriptions
tfidf = TfidfVectorizer(max_features=500)
X = tfidf.fit_transform(df['Problem_Description']).toarray()

# Save the vectorizer for later use
with open('preprocessing/vectorizer.pkl', 'wb') as f:
    pickle.dump(tfidf, f)

# Label encode the Category and Severity
le_category = LabelEncoder()
le_severity = LabelEncoder()

df['Category'] = le_category.fit_transform(df['Category'])
df['Severity'] = le_severity.fit_transform(df['Severity'])

# Define target variables
y_category = df['Category']
y_severity = df['Severity']

# Split the data
X_train, X_test, y_category_train, y_category_test = train_test_split(X, y_category, test_size=0.2, random_state=42)
_, _, y_severity_train, y_severity_test = train_test_split(X, y_severity, test_size=0.2, random_state=42)

# Build the category classification model
model_category = tf.keras.models.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(len(df['Category'].unique()), activation='softmax')
])

# Build the severity classification model
model_severity = tf.keras.models.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(len(df['Severity'].unique()), activation='softmax')
])

# Compile the models
model_category.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model_severity.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the models
model_category.fit(X_train, y_category_train, epochs=10, validation_data=(X_test, y_category_test))
model_severity.fit(X_train, y_severity_train, epochs=10, validation_data=(X_test, y_severity_test))

# Save the models
model_category.save('models/category_model.h5')
model_severity.save('models/severity_model.h5')
