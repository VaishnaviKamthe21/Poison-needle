import joblib
from responses import responses

model = joblib.load("chatbot_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

THRESHOLD = 0.5

def get_response(user_input):
    vec = vectorizer.transform([user_input])
    
    # probabilities for each class
    probs = model.predict_proba(vec)[0]
    intent = model.classes_[probs.argmax()]
    confidence = probs.max()
    
    if confidence < THRESHOLD or intent not in responses:
        # HTML link for Flask route
        return ("I don't have info on this. "
                "Please submit a request/complaint "
                "<a href='/complaint' target='_blank' style='color:#00f;'>here</a>.")
    
    return responses.get(intent)
