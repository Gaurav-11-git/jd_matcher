# file_readers/base_reader.py

class BaseReader:
    def read(self, file_storage):
        raise NotImplementedError("Subclasses must implement `read` method")
