# Team Name
AI Powered Job Description - Resume Matcher

## Overview
Welcome to our project submission for the Agentic AI incubation! This repository contains the code and documentation for our innovative solution. Our project aims to match the resumes against the job description to help in prioritizing the interview scheduling for the right candidates.

## Explanation
Our project leverages Open AI, Langchain, Agentic AI framework to create an AI powered web application for job description and resumes matching. The core functionality includes:
- **AI Compliance Report**: Provides ATS compliance report for each resume
- **Match %**: Resume matching % against JD
- **Algorithm Selection**: Allows selection of using AI and Non-AI algorithms 

## Intent
The primary intent of our project is to help the talent acquisition team to expedite the resume screening process.

## Use Case
Assigned Industry Use Case: HR/Talent Acquisition Team  
 
Our solution is designed to be used by HR/Talent Acquisition Team. It can be applied in scenarios such as:
- **Scenario 1**: Proper job description and resumes are available 
- **Scenario 2**: Short job description and some keywords are available along with resumes 


## Contributors

- **Bharat Panchal**: Solution Architect, Developer, All-in-one

## Images
Input :

Output : 

## Implementation
### Technologies Used
Python: The primary programming language for backend and UI development.

OpenAI: Utilized for text matching.

LangChain: A framework for building applications with language models.

Agentic AI Framework: For managing AI agents and their interactions.

Flask: For building the RESTful API.

Streamlit: UI building framework.
### Architecture
The architecture of the web application has be divided into several components:

Frontend: The user interface where recruiters can upload job descriptions and resumes, and view matching results.

Backend: The core of the application, responsible for processing job descriptions and resumes, and interacting with the AI/Non-AI agents.

AI Models: OpenAI models for NLP tasks such as text embedding, similarity scoring, and ranking.

API Layer: FlaskAPI to expose endpoints for the frontend to interact with the backend.

Agentic AI Framework: Manages the AI agents that handle different tasks such as text processing, matching, and ranking.

### Design Decisions
Modular Design: The application is designed in a modular fashion to ensure extensibility, scalability and maintainability. Each component has been developed as an agent.

Use of Pre-trained Models: Leveraging pre-trained models from OpenAI reduces the need for extensive training and allows for quick deployment.

Agentic AI Framework: Using an agentic AI framework allows for better management of AI agents, making it easier to handle complex interactions and workflows.

RESTful API: FlaskAPI is chosen for its ease of use, providing a robust API layer for the frontend to interact with the backend.


## Additional Information
Future Plan:
- Make the solution container based
- Provide resume comparison, quick resume summary 

