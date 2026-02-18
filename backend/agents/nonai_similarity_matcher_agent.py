# backend/agents/nonai_similarity_matcher_agent.py
from .base_agent import BaseAgent
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .logger_agent import LoggerAgent
from .log_level import LogLevel
class NonAiSimilarityMatcherAgent(BaseAgent):

    def __init__(self):
        self.logger = LoggerAgent()
    def run(self, jd_obj_list, resume_obj_list):
        self.logger.run("Starting matching process", LogLevel.INFO)
        jd_text = jd_obj_list[0].content
        resumes_texts = []
        for i, resume_obj in enumerate(resume_obj_list):
            resumes_texts.append(resume_obj.content)

        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([jd_text] + resumes_texts)
        jd_vector = vectors[0]
        resume_vectors = vectors[1:]
        scores = cosine_similarity(jd_vector, resume_vectors).flatten().tolist()

        for i, score in enumerate(scores):
            resume_obj_list[i].non_ai_score = score
            self.logger.run(f"resume_obj_list {resume_obj_list[i]} ", LogLevel.INFO)


        self.logger.run(f"Calculated similarity for {len(scores)} resumes", LogLevel.INFO)
        return scores

    def run1(self, jd_text, resumes_texts):
        self.logger.run("Starting matching process", LogLevel.INFO)
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([jd_text] + resumes_texts)
        jd_vector = vectors[0]
        resume_vectors = vectors[1:]
        scores = cosine_similarity(jd_vector, resume_vectors).flatten().tolist()
        self.logger.run(f"Calculated similarity for {len(scores)} resumes", LogLevel.INFO)
        return scores
