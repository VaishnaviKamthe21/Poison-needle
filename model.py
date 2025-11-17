import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import string

df = pd.read_csv("intents.csv")

def preprocess(text):
    text = text.lower()  
    text = text.translate(str.maketrans('', '', string.punctuation))  
    text = ' '.join(text.split())  
    return text

df['question'] = df['question'].apply(preprocess)

X = df['question']
y = df['intent']

vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1,2))
X_vec = vectorizer.fit_transform(X)

model = LogisticRegression(solver='lbfgs', multi_class='auto', max_iter=500)
model.fit(X_vec, y)

# Save
joblib.dump(model, "chatbot_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
