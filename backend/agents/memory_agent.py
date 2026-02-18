from datetime import datetime


from .base_agent import BaseAgent
from .logger_agent import LoggerAgent
from .log_level import LogLevel
import json
import os

class MemoryAgent(BaseAgent):
    def __init__(self, path="memory/match_history.json"):
        self.logger = LoggerAgent()
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            with open(path, "w") as f:
                json.dump([], f)

    def run(self, jd, resume_matches):
        self.logger.run("MemoryAgent: Storing match results...", LogLevel.INFO)
        with open(self.path, "r+") as f:
            history = json.load(f)
            history.append({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "jd": jd, "matches": resume_matches})
            f.seek(0)
            json.dump(history, f, indent=2)
