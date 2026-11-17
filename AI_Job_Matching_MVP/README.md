# AI Job Matching MVP — Windows Setup Guide

## Files
- `app.py` — the application
- `requirements.txt` — required Python packages

## Step 1: Extract the ZIP
1. Open your **Downloads** folder in File Explorer.
2. Right-click `AI_Job_Matching_MVP.zip`.
3. Choose **Extract All...** and click **Extract**.
4. You should get a folder named `AI_Job_Matching_MVP`.

## Step 2: Open the folder in VS Code
1. Open VS Code.
2. Click **File → Open Folder**.
3. Select the extracted `AI_Job_Matching_MVP` folder (not the ZIP file).
4. In the left Explorer panel, you should see `app.py`, `requirements.txt`, and `README.md`.

## Step 3: Open the VS Code terminal
Click **Terminal → New Terminal**. Make sure the terminal is working inside the `AI_Job_Matching_MVP` folder.

## Step 4: Create a virtual environment
Run:
```powershell
python -m venv .venv
```

## Step 5: Activate it
In the VS Code PowerShell terminal, run:
```powershell
.venv\Scripts\Activate.ps1
```
If PowerShell blocks activation, switch the terminal dropdown to **Command Prompt** and run:
```cmd
.venv\Scripts\activate.bat
```

## Step 6: Install packages
Run:
```bash
python -m pip install -r requirements.txt
```
Wait until installation finishes.

## Step 7: Run the app
Run:
```bash
python -m streamlit run app.py
```
A browser tab should open. If it does not, copy the Local URL shown in the terminal (usually `http://localhost:8501`) into Chrome.

## If Python is not recognized
Install Python from https://www.python.org/downloads/. During installation, tick **Add Python to PATH**. Restart VS Code. Then check:
```bash
py --version
```
If `py` works, replace `python` with `py` in the commands above.

## Important
This is a starter MVP, not a completed production platform. It uses sample jobs, a fixed skill keyword list, and text similarity. It does not yet include authentication, OCR for scanned resumes, live job listings, or MongoDB storage. The current app is Python + Streamlit, not the planned React + Node.js full-stack version.
