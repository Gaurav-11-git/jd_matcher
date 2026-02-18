# matchers/jd_resume_matcher.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class JDResumeMatcher:
    def __init__(self, jd_text, resume_texts):
        self.jd_text = jd_text
        self.resume_texts = resume_texts

    def match(self):
        documents = [self.jd_text] + self.resume_texts
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(documents)

        jd_vector = tfidf_matrix[0]
        resume_vectors = tfidf_matrix[1:]

        similarities = cosine_similarity(jd_vector, resume_vectors).flatten()

        results = []
        for idx, score in enumerate(similarities):
            results.append({
                "resume_index": idx,
                "score": round(float(score), 4)
            })

        results = sorted(results, key=lambda x: x["score"], reverse=True)
        return results
