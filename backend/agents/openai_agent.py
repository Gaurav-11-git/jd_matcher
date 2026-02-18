# openai_agent.py

import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from .logger_agent import LoggerAgent
from .log_level import LogLevel

class OpenAIAgent:
    def __init__(self):
        load_dotenv()
        self.logger = LoggerAgent()

        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", "0"))
        self.api_version = os.getenv("OPENAI_API_VERSION")
        self.api_endpoint = os.getenv("OPENAI_API_BASE")

        if not self.api_key:
            self.logger.run("OpenAIAgent: OPENAI_API_KEY not set in .env!", LogLevel.ERROR)
            raise ValueError("Missing OpenAI API Key")

        self.client = AzureOpenAI(
                    api_version=self.api_version,
                    azure_endpoint=self.api_endpoint,
                    api_key=self.api_key,
        )

    def chat(self, prompt, system_message="You are a helpful assistant."):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature
            )
            reply = response.choices[0].message.content.strip()
            self.logger.run("OpenAIAgent: Response received.", LogLevel.DEBUG)
            return reply

        except Exception as e:
            self.logger.run(f"OpenAIAgent Error: {str(e)}", LogLevel.ERROR)
            return None
