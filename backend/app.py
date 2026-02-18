from flask import Flask, request, jsonify
from flask_cors import CORS

from backend.agents.log_level import LogLevel
from backend.agents.logger_agent import LoggerAgent
from backend.agents.orchestrator_agent import OrchestratorAgent
from backend.entities.uploaded_file import UploadedFile
from backend.entities.uploaded_file_type import UploadedFileType

app = Flask(__name__)
CORS(app)
orchestrator = OrchestratorAgent()
logger = LoggerAgent()

def populateUploadedFileObjList(uploaded_files, file_type):
    obj_list = []
    for file in uploaded_files:
        obj_list.append(UploadedFile(file_type=file_type, file_obj=file, file_name=None, extension=None, content=None, size=None))
    print("file_type = ", file_type)
    print("obj_list = ", obj_list)
    return obj_list


@app.route("/match", methods=["POST"])
def match():
    print("match API called...")

    # Parse parameters
    alpha = float(request.args.get("alpha", 0.5))
    methods_param = request.args.get("methods", "ai")  # default to AI if not provided
    required_keywords = request.args.get("keywords", "")

    print("required_keywords = ", required_keywords)

    methods = [m.strip().lower() for m in methods_param.split(",")]

    # Get files
    jd_files = request.files.getlist("jd_file")
    resume_files = request.files.getlist("resumes")

    if not jd_files or not resume_files:
        return jsonify({"error": "Missing JD or resumes"}), 400

    # Run orchestrator with method list

    jd_obj_list = populateUploadedFileObjList(uploaded_files=jd_files, file_type=UploadedFileType.JOB_DESCRIPTION.value)
    resume_obj_list = populateUploadedFileObjList(uploaded_files=resume_files, file_type=UploadedFileType.RESUME.value)
    result = orchestrator.run(jd_obj_list=jd_obj_list,
                              resume_obj_list=resume_obj_list, methods=methods, required_keywords=required_keywords)

    response = {
        "total_resumes": len(resume_files)
    }

    if "ai" in result:
        response["ai_results"] = result["ai"]
    if "traditional" in result:
        response["traditional_results"] = result["traditional"]

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
