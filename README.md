🚀 AI Resume & Cover Letter Generator (Desktop App)
This is a Python-based desktop application built with Tkinter and ReportLab that utilizes the Google Gemini API to quickly generate professional resume summaries, bullet points, project descriptions, and custom cover letters based on user inputs.

The application packages the entire resume and cover letter into a clean, ready-to-print PDF document.

✨ Features
AI Content Generation: Uses Gemini-2.5-Flash to craft professional summaries, action-verb-driven bullet points for work experience, and impactful project descriptions.

PDF Generation: Exports a single, professionally formatted PDF file for the resume and cover letter.

Dynamic UI: Allows users to add multiple work experience, project, and certification entries.

Hyperlinking: Automatically formats contact links (LinkedIn, URLs, etc.) as clickable hyperlinks in the final PDF.

⚙️ Installation (Run from Source)
Clone the repository:

git clone [https://github.com/Vivek-Jha-05/AI-Resume-Generator.git](https://github.com/Vivek-Jha-05/AI-Resume-Generator.git)
cd AI-Resume-Generator

Install dependencies:

pip install -r requirements.txt

Set your API Key:

Get a Gemini API Key from Google AI Studio.

Open app.py and replace the placeholder value in the API_KEY variable with your actual key.

Run the application:

python app.py

📦 Deployment (Creating a Standalone Executable)
To allow users to run the app without installing Python, use PyInstaller.

Ensure PyInstaller is installed (included in requirements.txt).

Run the following command in your terminal:

pyinstaller --onefile --windowed app.py

--onefile: Packages everything into a single executable file.

--windowed: Prevents a terminal window from opening alongside the GUI (for Windows/Mac).

The final executable (app.exe or app) will be located in the newly created dist/ folder.
