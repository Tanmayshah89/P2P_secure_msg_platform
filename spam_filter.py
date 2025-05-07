import re
import joblib

# Load the trained model and vectorizer
model = joblib.load('model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Text Cleaning (based on common preprocessing patterns)
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)          # Remove special characters
    text = re.sub(r'\s+', ' ', text)         # Replace multiple spaces with single
    return text.strip()

# Spam Detection Function
def is_spam(message):
    cleaned = clean_text(message)
    vector = vectorizer.transform([cleaned])
    prediction = model.predict(vector)
    return prediction[0] == 1  # 1 = spam, 0 = ham

