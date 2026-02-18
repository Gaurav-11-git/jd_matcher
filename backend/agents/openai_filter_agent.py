import json
from .base_agent import BaseAgent
from .logger_agent import LoggerAgent
from .log_level import LogLevel
from .openai_agent import OpenAIAgent

class OpenAiFilterAgent(BaseAgent):
    def __init__(self):
        self.logger = LoggerAgent()
        self.openai_agent = OpenAIAgent()

    def run(self, jd_obj_list, resume_obj_list):
        self.logger.run("OpenAiFilterAgent: Evaluating resumes using OpenAI...", LogLevel.INFO)

        ai_results = []
        jd_text = jd_obj_list[0].content
        for i, resume_obj in enumerate(resume_obj_list):
            resume = resume_obj.content
            prompt = (
                "You are an expert recruiter. Given a job description and a candidate resume, assess whether the candidate is a good fit.\n"
                "Respond in the following strict JSON format:\n"
                "{\n"
                '  "fit": "Yes" or "No",\n'
                '  "reason": "Explanation if No, otherwise leave empty"\n'
                "}\n\n"
                f"Job Description:\n{jd_text}\n\nResume:\n{resume}"
            )

            response = self.openai_agent.chat(prompt)

            accepted = False
            decision = "no"
            reason = "No reason provided"

            try:
                parsed = json.loads(response)
                decision = parsed.get("fit", "").strip().lower()
                reason = parsed.get("reason", "").strip()
                accepted = decision == "yes"
                resume_obj.ai_selected = accepted
                resume_obj.ai_reason = reason if not accepted else ""
            except Exception as e:
                self.logger.run(f"Failed to parse response as JSON: {response}", LogLevel.ERROR)

            ai_results.append({
                "resume_text": resume,
                "accepted_by_openai": accepted,
                "decision": decision,
                "reason": reason if not accepted else ""
            })

            self.logger.run(
                f"Resume {i+1} {'accepted' if accepted else 'rejected'} by OpenAI. Reason: {reason}",
                LogLevel.DEBUG
            )

        self.logger.run(
            f"OpenAiFilterAgent: {sum(r['accepted_by_openai'] for r in ai_results)} accepted out of {len(ai_results)}.",
            LogLevel.INFO
        )

        return ai_results
