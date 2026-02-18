# backend/agents/parser_agent.py
from .base_agent import BaseAgent
from ..file_readers.file_reader_factory import FileReaderFactory
from .logger_agent import LoggerAgent
from .log_level import LogLevel

class ParserAgent(BaseAgent):
    def __init__(self):
        self.logger = LoggerAgent()
    def run(self, uploaded_file_obj_list):
        results = []
        for uploaded_file in uploaded_file_obj_list:
            ext = uploaded_file.file_obj.filename.split('.')[-1].lower()
            uploaded_file.extension = ext
            uploaded_file.file_name = uploaded_file.file_obj.filename
            self.logger.run(f"Parsing file: {uploaded_file.file_obj.filename} (.{ext})", LogLevel.DEBUG)
            reader = FileReaderFactory.get_reader(uploaded_file.file_obj.filename)
            if reader:
                content = reader.read(uploaded_file.file_obj)
                uploaded_file.content = content
                results.append(content)
            else:
                self.logger.run(f"No reader found for extension: .{ext}", LogLevel.WARNING)
            self.logger.run(f"UploadedFileObj = {uploaded_file}")
        return results
