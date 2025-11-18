from sentence_transformers import SentenceTransformer, util
import pandas as pd
from responses import responses

df = pd.read_csv("intents.csv")

all_examples = df["question"].tolist()
example_intents = df["intent"].tolist()

model = SentenceTransformer('all-MiniLM-L6-v2')  
example_embeddings = model.encode(all_examples)  

def best_intent(user_input):
    user_emb = model.encode([user_input])[0]
    
    sims = util.cos_sim(user_emb, example_embeddings)[0]
    best_idx = sims.argmax().item()
    best_score = sims[best_idx].item()
    if best_score < 0.55:  
        return None
    return example_intents[best_idx]

def get_response(user_input):
    intent = best_intent(user_input)
    if not intent or intent not in responses:
        return ("I don't have info on this. "
                "Please submit a request/complaint "
                "<a href='/complaint' target='_blank' style='color:#00f;'>here</a>.")
    return responses[intent]
