import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf

# Load the CSV data
df = pd.read_csv('data/ticket_data.csv')

# Debug: Print column names to ensure they match the CSV file
print("Columns in the dataset:", df.columns)

# Ensure the column names are correct
X = df['Problem Description']  # Features (Input text)
y_category = df['Category']    # Labels for category
y_severity = df['Severity']    # Labels for severity

# Step 1: Preprocess the text data using TF-IDF
tfidf = TfidfVectorizer(max_features=500)  # Limiting to top 500 features
X_tfidf = tfidf.fit_transform(X).toarray()

# Step 2: Encode the labels (Category and Severity) into integers
label_encoder_category = LabelEncoder()
y_category_encoded = label_encoder_category.fit_transform(y_category)

label_encoder_severity = LabelEncoder()
y_severity_encoded = label_encoder_severity.fit_transform(y_severity)

# Step 3: Train-test split (using 80% for training and 20% for testing)
X_train, X_test, y_train_cat, y_test_cat, y_train_sev, y_test_sev = train_test_split(
    X_tfidf, y_category_encoded, y_severity_encoded, test_size=0.2, random_state=42
)

# Step 4: Define Input layer
input_layer = Input(shape=(X_tfidf.shape[1],))

# Step 5: Build a simple neural network model using Keras
dense_layer_1 = Dense(128, activation='relu')(input_layer)
dropout_layer_1 = Dropout(0.5)(dense_layer_1)
dense_layer_2 = Dense(64, activation='relu')(dropout_layer_1)
dropout_layer_2 = Dropout(0.5)(dense_layer_2)
dense_layer_3 = Dense(32, activation='relu')(dropout_layer_2)

# Separate outputs for category and severity
category_output = Dense(len(label_encoder_category.classes_), activation='softmax', name='category_output')(dense_layer_3)
severity_output = Dense(len(label_encoder_severity.classes_), activation='softmax', name='severity_output')(dense_layer_3)

# Step 6: Create model
model = Model(inputs=input_layer, outputs={'category_output': category_output, 'severity_output': severity_output})

# Step 7: Compile the model
model.compile(optimizer='adam',
              loss={'category_output': 'sparse_categorical_crossentropy', 
                    'severity_output': 'sparse_categorical_crossentropy'},
              metrics=['accuracy'])

# Step 8: Use EarlyStopping to prevent overfitting
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# Step 9: Train the model
history = model.fit(X_train, 
                    {'category_output': y_train_cat, 'severity_output': y_train_sev},
                    epochs=50, 
                    validation_data=(X_test, {'category_output': y_test_cat, 'severity_output': y_test_sev}),
                    callbacks=[early_stopping])

# Step 10: Save the trained model using the .keras format (new Keras format)
model.save('model/ticket_classifier.keras')

# Optional: Save the label encoders as well so you can decode the predictions later
import pickle
with open('model/category_label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder_category, f)

with open('model/severity_label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder_severity, f)

print("Model training complete and saved as 'ticket_classifier.keras'.")
