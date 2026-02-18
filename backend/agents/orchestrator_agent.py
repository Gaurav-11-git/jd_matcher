from .knowledge_agent import KnowledgeAgent
from .logger_agent import LoggerAgent
from .log_level import LogLevel
from .nonai_ats_compliance_checker_agent import NonAiAtsComplianceCheckerAgent
from .nonai_similarity_matcher_agent import NonAiSimilarityMatcherAgent
from .memory_agent import MemoryAgent
from .nonai_filter_agent import NonAiFilterAgent
from .parser_agent import ParserAgent
from .openai_filter_agent import OpenAiFilterAgent

class OrchestratorAgent:
    def __init__(self):
        self.parser_agent = ParserAgent()
        self.open_ai_filter = OpenAiFilterAgent()
        self.non_ai_filter_agent = NonAiFilterAgent()
        self.non_ai_similarity_matcher_agent = NonAiSimilarityMatcherAgent()
        self.non_ai_ats_compliance_checker_agent = NonAiAtsComplianceCheckerAgent()
        self.logger = LoggerAgent()
        self.knowledge = KnowledgeAgent()
        self.memory = MemoryAgent()

    def run(self, jd_obj_list, resume_obj_list, methods=["ai"], required_keywords=""):
        self.logger.run("Orchestration started: JD + Resumes", LogLevel.INFO)

        jd_text = self.parser_agent.run(jd_obj_list)[0]
        resume_texts = self.parser_agent.run(resume_obj_list)

        self.logger.run(f"After parsing, JD = {jd_obj_list}")
        self.logger.run(f"After parsing, RESUME = {resume_obj_list}")

        self.logger.run(f"JD parsed with length {len(jd_text)}", LogLevel.DEBUG)
        self.logger.run(f"{len(resume_texts)} resumes parsed", LogLevel.DEBUG)

        results = {}

        if "ai" in methods or "both" in methods:
            self.logger.run("Running AI-based filtering", LogLevel.INFO)
            self.open_ai_filter.run(jd_obj_list, resume_obj_list)

            ai_results = []
            for i, r in enumerate(resume_obj_list):
                ai_results.append({
                    "resume_index": i,
                    "resume_name" : r.file_name,
                    "accepted_by_openai": r.ai_selected,
                    "reason": r.ai_reason
                })

            results["ai"] = ai_results
            self.memory.run(jd_text, ai_results)

        if "traditional" in methods or "both" in methods:
            self.logger.run("Running traditional (non-AI) filtering", LogLevel.INFO)
            self.non_ai_filter_agent.run(jd_obj_list, resume_obj_list)
            self.non_ai_ats_compliance_checker_agent.run(jd_obj_list, resume_obj_list, required_keywords)
            # Get only accepted resumes for scoring
            # trad_filtered = self.non_ai_filter_agent.run(jd_obj_list, resume_obj_list)
            # accepted_texts = [r["resume_text"] for r in trad_filtered if r.get("accepted_by_rule")]

            self.non_ai_similarity_matcher_agent.run(jd_obj_list, resume_obj_list)
            self.knowledge.run(jd_obj_list, resume_obj_list)

            trad_results = []

            for i, r in enumerate(resume_obj_list):
                trad_results.append({
                    "resume_index": i,
                    "resume_name": r.file_name,
                    "accepted_by_rule": r.non_ai_selected,
                    "tfidf_score": r.non_ai_score,
                    "semantic_score": r.non_ai_semantic_score,
                    "reason": r.non_ai_reason,
                    "ats_compliance_report": r.non_ai_ats_compliance_report
                })

            results["traditional"] = trad_results
            self.memory.run(jd_text, trad_results)

        self.logger.run("Orchestration complete", LogLevel.INFO)
        print(results)
        return results
