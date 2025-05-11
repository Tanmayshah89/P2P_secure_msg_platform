# spam_filter.py

import pickle
import os
import sys

# Ensure the required model and vectorizer files exist
model_path = "model.pkl"
vectorizer_path = "vectorizer.pkl"

if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
    print("[ERROR] Required model files not found. Make sure 'model.pkl' and 'vectorizer.pkl' exist.")
    sys.exit(1)

# Load the vectorizer and model
try:
    with open(vectorizer_path, "rb") as vec_file:
        vectorizer = pickle.load(vec_file)
    with open(model_path, "rb") as model_file:
        model = pickle.load(model_file)
except Exception as e:
    print(f"[ERROR] Failed to load model/vectorizer: {e}")
    sys.exit(1)

# Function to check spam
def is_spam(text):
    try:
        x = vectorizer.transform([text])
        prediction = model.predict(x)[0]
        return prediction == 1
    except Exception as e:
        print(f"[ERROR] Spam detection failed: {e}")
        return False
