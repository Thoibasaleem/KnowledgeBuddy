import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_recommendations():
    json_path = os.path.join(os.path.dirname(__file__), 'recommendations.json')
    with open(json_path, 'r') as file:
        return json.load(file)

def generate_recommendations(backlogs, weak_subjects):
    data = load_recommendations()
    input_text = f"{backlogs} {weak_subjects}"
    corpus = [entry["topic"] for entry in data]

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(corpus + [input_text])
    similarity_scores = cosine_similarity(vectors[-1], vectors[:-1]).flatten()

    top_indices = similarity_scores.argsort()[-3:][::-1]
    top_recommendations = [data[i] for i in top_indices if similarity_scores[i] > 0]

    return top_recommendations
