# file_readers/docx_reader.py

from docx import Document
from .base_reader import BaseReader

class DocxReader(BaseReader):
    def read(self, file_storage):
        doc = Document(file_storage)
        return "\n".join([para.text for para in doc.paragraphs])
