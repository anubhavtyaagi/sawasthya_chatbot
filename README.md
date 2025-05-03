# sawasthya_chatbot
HealthCare ChatBot
A Streamlit-based web application that assists users in diagnosing potential medical conditions based on symptoms using machine learning models (Decision Tree and SVM). The chatbot provides preliminary diagnoses, severity assessments, and precautionary measures.
Table of Contents

Overview
Features
Requirements
Installation
Directory Structure
Running the Application
Usage
Troubleshooting
Contributing
License

Overview
The HealthCare ChatBot is designed to help users identify potential health issues by inputting symptoms. It uses a Decision Tree classifier trained on a medical dataset to predict possible conditions, supplemented by an SVM model for validation. The app also provides symptom severity assessments and precautionary advice based on data from CSV files.
Features

Symptom-Based Diagnosis: Users input symptoms, and the app predicts possible medical conditions.
Severity Assessment: Evaluates the severity of symptoms based on duration and predefined weights.
Precautionary Advice: Provides actionable precautions for predicted conditions.
Interactive UI: Built with Streamlit for a user-friendly web interface.
Role-Based Integration: Can be linked to an EHR system (e.g., via a React app) for healthcare professionals.

Requirements

Python: Version 3.7 or higher (tested with Python 3.12).
Dependencies:
streamlit>=1.12.0
pandas
scikit-learn
numpy


Data Files:
Data/Training.csv
Data/Testing.csv
MasterData/symptom_severity.csv
MasterData/symptom_Description.csv
MasterData/symptom_precaution.csv



Installation

Clone the Repository (if not already done):
git clone <repository-url>
cd healthcare-chatbot


Set Up a Virtual Environment (recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:Create a requirements.txt file with:
streamlit>=1.12.0
pandas
scikit-learn
numpy

Then run:
pip install -r requirements.txt


Verify Data Files:Ensure the following files are in the correct directories:

Data/Training.csv
Data/Testing.csv
MasterData/symptom_severity.csv
MasterData/symptom_Description.csv
MasterData/symptom_precaution.csv



Directory Structure
healthcare-chatbot/
├── Data/
│   ├── Training.csv
│   ├── Testing.csv
├── MasterData/
│   ├── symptom_severity.csv
│   ├── symptom_Description.csv
│   ├── symptom_precaution.csv
├── streamlit_app.py
├── requirements.txt
├── README.md

Running the Application

Start the Streamlit Server:
streamlit run streamlit_app.py

The app will launch in your default browser at http://localhost:8501.

Verify Accessibility:

Ensure the app loads and displays the "HealthCare ChatBot" title.
If the port 8501 is in use, Streamlit will suggest an alternative port, or you can specify one:streamlit run streamlit_app.py --server.port 8502





Usage

Enter Your Name:
Input your name and click "Submit Name".


Input a Symptom:
Enter a symptom (e.g., "fever") and click "Submit Symptom".


Confirm Symptom:
If multiple matches are found, select the correct symptom from the dropdown and click "Confirm Symptom".


Specify Duration:
Enter the number of days you’ve experienced the symptom and click "Submit Days".


Answer Additional Questions:
Respond "Yes" or "No" to additional symptoms prompted by the app.


Get Diagnosis:
Click "Get Diagnosis" to view the predicted condition, severity advice, and precautions.


Restart:
Click "Restart" to begin a new session.



Troubleshooting

File Not Found Errors:
Verify that all CSV files are in the Data/ and MasterData/ directories.
Check file paths in streamlit_app.py if you’ve modified the directory structure.


Module Not Found:
Ensure all dependencies are installed (pip install -r requirements.txt).
Check Python version compatibility (3.7+).


KeyError for Symptoms:
Ensure symptom_severity.csv contains all symptoms listed in Training.csv.
Verify data consistency in CSV files.


Port Conflicts:
Use a different port if 8501 is occupied:streamlit run streamlit_app.py --server.port 8502




App Not Loading:
Check the terminal for error messages.
Ensure the browser allows http://localhost:8501.



Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a feature branch (git checkout -b feature/your-feature).
Commit changes (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a pull request.

Please ensure your code follows the project’s style and includes tests where applicable.
License
This project is licensed under the MIT License. See the LICENSE file for details (if available in the repository).

Built with Streamlit for healthcare accessibility.
