# file_readers/file_reader_factory.py

from .docx_reader import DocxReader
from .pdf_reader import PDFReader
from .base_reader import BaseReader

class DefaultReader(BaseReader):
    def read(self, file_storage):
        return file_storage.read().decode("utf-8", errors="ignore")

class FileReaderFactory:
    @staticmethod
    def get_reader(filename: str) -> BaseReader:
        filename = filename.lower()

        if filename.endswith(".docx"):
            return DocxReader()
        elif filename.endswith(".pdf"):
            return PDFReader()
        else:
            return DefaultReader()

    @staticmethod
    def read_text(file_storage):
        reader = FileReaderFactory.get_reader(file_storage.filename)
        return reader.read(file_storage)
