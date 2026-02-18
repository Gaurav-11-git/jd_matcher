# file_readers/pdf_reader.py

import fitz  # PyMuPDF
from .base_reader import BaseReader

class PDFReader(BaseReader):
    def read(self, file_storage):
        text = ""
        with fitz.open(stream=file_storage.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text
