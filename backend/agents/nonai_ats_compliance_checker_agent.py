from .base_agent import BaseAgent
from .log_level import LogLevel
from .logger_agent import LoggerAgent

# Automated Tracking Systems (ATS) are used by many companies to filter resumes before they reach human eyes.
# An ATS-compliant resume is one that is formatted and keyword-optimized in a way that allows it to be easily
# read and picked up by these systems
class NonAiAtsComplianceCheckerAgent(BaseAgent):
    def __init__(self):
        self.logger = LoggerAgent()

    def run(self, jd_obj_list, resume_obj_list, required_keywords):
        self.logger.run("NonAiAtsComplianceCheckerAgent: Checking ATS compliance without using AI...",
                        level=LogLevel.INFO)

        # Split the comma-separated keywords into a list
        keywords_list = [keyword.strip().lower() for keyword in required_keywords.split(",")]
        self.logger.run(f"Keywords list = {keywords_list}")

        for i, resume_obj in enumerate(resume_obj_list):
            resume_content = resume_obj.content.lower()

            keywords_found = [word for word in keywords_list if word in resume_content]
            self.logger.run(f"Keywords found = {keywords_found}")
            report = {
                "has_contact_info": any(word in resume_content for word in ["email", "phone", "address"]),
                "has_summary": "summary" in resume_content,
                "has_experience": "experience" in resume_content,
                "has_education": "education" in resume_content,
                "has_skills": "skills" in resume_content,
                "keywords_found": ", ".join(keywords_found),
                "keyword_density": len(keywords_found) / len(resume_content.split())
            }
            resume_obj.non_ai_ats_compliance_report = report

        self.logger.run("NonAiAtsComplianceCheckerAgent: Completed checking ATS compliance without "
                        "using AI...", level=LogLevel.INFO)
