from .base_agent import BaseAgent
from .log_level import LogLevel
from .logger_agent import LoggerAgent

class NonAiFilterAgent(BaseAgent):
    def __init__(self):
        self.logger = LoggerAgent()

    def run(self, jd_obj_list, resume_obj_list):
        self.logger.run("NonAiFilterAgent: Filtering resumes without using AI...", level=LogLevel.INFO)

        results = []
        for i, resume_obj in enumerate(resume_obj_list):
            resume = resume_obj.content
            word_count = len(resume.split())
            accepted = word_count > 50  # Simple rule-based logic
            resume_obj.non_ai_selected = accepted
            resume_obj.non_ai_reason = f"Resume {'accepted' if accepted else 'rejected'} by rule-based filter (word count: {word_count})"
            results.append({
                "resume_text": resume,
                "accepted_by_rule": accepted,
                "reason": f"Word count: {word_count}"
            })

            self.logger.run(
                f"Resume {i+1} {'accepted' if accepted else 'rejected'} by rule-based filter (word count: {word_count})",
                level=LogLevel.DEBUG
            )

        self.logger.run(
            f"NonAiFilterAgent: {sum(r['accepted_by_rule'] for r in results)} accepted out of {len(results)}.",
            level=LogLevel.INFO
        )
        return results
