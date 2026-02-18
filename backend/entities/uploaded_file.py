class UploadedFile:
    def __init__(self, file_type, file_obj, file_name, extension, content, size):
        self.file_type = file_type
        self.file_obj = file_obj
        self.file_name = file_name
        self.extension = extension
        self.content = content
        self.size = size
        self.ai_selected = False
        self.ai_reason = ''
        self.non_ai_selected = False
        self.non_ai_reason = ''
        self.non_ai_score = 0
        self.non_ai_semantic_score = 0
        self.non_ai_ats_compliance_report = None


    def __str__(self):
         return (
             f"Type: {self.file_type}\n"
             f"File Name: {self.file_name}\n"
             f"Extension: {self.extension}\n"
             f"Size: {self.size} bytes\n"
             f"ai_selected: {self.ai_selected}\n"
             f"ai_reason: {self.ai_reason}\n"
             f"non_ai_selected: {self.non_ai_selected}\n"
             f"non_ai_score: {self.non_ai_score}\n"
             f"non_ai_semantic_score: {self.non_ai_semantic_score}\n"
             f"non_ai_ats_compliance_report: {self.non_ai_ats_compliance_report}\n"
             # f"Content: {self.content}"
         )

    def display_info(self):
        print(f"File Name: {self.file_name}")
        print(f"Extension: {self.extension}")
        print(f"Size: {self.size} bytes")

    def get_content(self):
        return self.content

# Example usage:
uploaded_file_obj = UploadedFile("RESUME", None, "John_Doe_Resume", ".pdf",
                                 "This is the content of the resume.", 2048)
uploaded_file_obj.display_info()
print("Content:", uploaded_file_obj.get_content())
