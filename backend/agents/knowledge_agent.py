from .base_agent import BaseAgent
from .logger_agent import LoggerAgent
from .log_level import LogLevel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class KnowledgeAgent(BaseAgent):
    def __init__(self):
        self.logger = LoggerAgent()
        # TODO: Add real OpenAI key or SentenceTransformer
        # self.embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

    def embed(self, text):
        # Placeholder: random vector
        return np.random.rand(512)

    def run(self, jd_obj_list, resume_obj_list):
        self.logger.run("KnowledgeAgent: Computing semantic similarity...", LogLevel.INFO)
        jd_text = jd_obj_list[0].content
        resumes_texts = []
        for i, resume_obj in enumerate(resume_obj_list):
            resumes_texts.append(resume_obj.content)
        jd_vec = self.embed(jd_text)
        resume_vecs = [self.embed(res) for res in resumes_texts]
        similarities = cosine_similarity([jd_vec], resume_vecs).flatten()

        for i, score in enumerate(similarities):
            resume_obj_list[i].non_ai_semantic_score = score
            self.logger.run(f"resume_obj_list {resume_obj_list[i]} ", LogLevel.INFO)

        return list(enumerate(similarities))
