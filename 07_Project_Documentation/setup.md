# Setup & Installation Guide - NetConnect

This guide walks you through setting up the local development environment for **NetConnect (Personalized Networking Assistant)**.

---

## 1. Prerequisites

Make sure you have the following installed on your machine:
- **Python**: Version `3.8` to `3.11` is recommended.
- **Git**: Installed and configured on your path.

---

## 2. Step-by-Step Setup

### Step 1: Clone the Repository
Clone your repository locally and navigate to the project directory:
```bash
git clone https://github.com/SurendraBehra/Personalized-Networking-Assistant.git
cd Personalized-Networking-Assistant
```

### Step 2: Create a Virtual Environment
It is highly recommended to isolate your dependencies inside a virtual environment:
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
Navigate into the development directory and install required libraries:
```bash
cd 05_Project_Development
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Copy the `.env.example` file to `.env` inside the `05_Project_Development/` directory:
```bash
# On Windows PowerShell (run inside 05_Project_Development)
Copy-Item .env.example .env

# On macOS/Linux/Bash (run inside 05_Project_Development)
cp .env.example .env
```

Open the newly created `.env` file and fill in your details:
```env
HOST=127.0.0.1
PORT=8000
DATABASE_URL=sqlite:///./networking_assistant.db

# Insert your Gemini API Key from Google AI Studio. 
# If left empty, NetConnect will seamlessly fall back to rule-based offline templates.
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 3. Running the Project

You can start both the Backend (FastAPI) and Frontend (Streamlit) using the convenient, unified launcher script. Run this command from within the `05_Project_Development/` directory:
```bash
cd 05_Project_Development
python run.py
```

This starts:
- **FastAPI Backend API**: Running at `http://127.0.0.1:8000`
- **Streamlit Web Application**: Running at `http://127.0.0.1:8501`

To stop both services at any time, simply press `Ctrl+C` in your terminal.

---

## 4. Running Backend Tests

Run the test suite using Python's built-in `unittest` module from inside `05_Project_Development/`:
```bash
cd 05_Project_Development
python -m unittest discover -s backend/tests
```
