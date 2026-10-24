# Automated Resume Parser 📄

A simple, beginner-friendly Python web application that extracts candidate information from PDF resumes and stores it in a searchable SQLite database.

Built as an internship project using Python, Streamlit, PDFPlumber, Regular Expressions, and SQLite.

---

## 📌 Project Overview

Recruiters often have to go through dozens of resumes manually to extract basic information such as candidate names, contact details, degrees, and skills. 

This **Automated Resume Parser** streamlines this process:
1. Allows uploading resumes in PDF format.
2. Automatically extracts key information: **Name, Email, Phone Number, Skills, and Education**.
3. Displays the extracted details in an editable form for verification.
4. Saves candidate records in a local **SQLite** database.
5. Displays all saved candidates in a searchable table.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python** | Core programming language |
| **Streamlit** | Interactive web user interface |
| **PDFPlumber** | Extracting raw text from PDF files |
| **Regular Expressions (`re`)** | Pattern matching for emails and phone numbers |
| **Keyword Matching** | Identifying candidate skills and education qualifications |
| **SQLite3** | Lightweight built-in relational database to store records |

---

## 📁 Project Structure

```text
resume/
│
├── app.py              # Streamlit web application interface
├── parser.py           # Text extraction, regex patterns, and keyword matching logic
├── database.py         # SQLite database initialization, insertion, and queries
├── requirements.txt    # Required external Python libraries
└── README.md           # Documentation, setup guide, and project explanation
```

---

## 🚀 Setup and Installation Instructions (Windows & VS Code)

Follow these step-by-step instructions to set up and run the project in Visual Studio Code on Windows:

### Step 1: Open the Project in VS Code
1. Open **Visual Studio Code**.
2. Click **File** > **Open Folder...**
3. Select your project folder: `c:\Users\mukta\OneDrive\Desktop\resume`.

### Step 2: Open the Integrated Terminal
- In VS Code, press `Ctrl + \`` (backtick) or go to the top menu and select **Terminal** > **New Terminal**.
- Ensure the terminal is pointing to your `resume` directory.

### Step 3: (Recommended) Create and Activate a Virtual Environment
In the VS Code terminal, run:

```powershell
python -m venv venv
```

Activate the virtual environment:
```powershell
.\venv\Scripts\Activate.ps1
```
*(If you get an execution policy error in PowerShell, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and then run the activate command again).*

### Step 4: Install Required Packages
Run the following command to install Streamlit and PDFPlumber:

```powershell
pip install -r requirements.txt
```

### Step 5: Run the Streamlit Application
Start the application using:

```powershell
streamlit run app.py
```

The web application will automatically open in your default web browser at:
`http://localhost:8501`

---

## 💡 How It Works (Mentor Explanation)

When explaining this project to your internship mentor, you can highlight these four key components:

### 1. PDF Text Extraction (`parser.py`)
- The function `extract_text_from_pdf()` uses `pdfplumber.open()` to open the uploaded PDF document.
- It iterates through each page of the document and extracts the text content using `page.extract_text()`.
- The extracted text from all pages is concatenated into a single string.

### 2. Information Extraction (`parser.py`)
- **Name Extraction**: In standard resumes, candidate names are located in the first few lines. The function `extract_name()` inspects the first five non-empty lines, skips generic headers (like "Resume" or "CV"), ignores lines with emails or numbers, and extracts the candidate's name.
- **Email Extraction**: Uses Python's built-in `re` module with the regex pattern `[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+` to detect standard email formats.
- **Phone Number Extraction**: Uses regex `(?:\+?\d{1,3}[\s-]?)?\(?\d{3,5}\)?[\s.-]?\d{3,5}[\s.-]?\d{3,5}` to detect standard 10-digit mobile numbers as well as numbers with country codes (such as `+91`).
- **Skills Identification**: Compares words in the resume against a predefined list of technical and soft skills (`COMMON_SKILLS`) using regex word boundary matching (`\b...\b`) to avoid false substring matches.
- **Education Identification**: Searches for common degree abbreviations and full names (such as `B.Tech`, `MCA`, `B.Sc`, `MBA`, etc.) using keyword matching.

### 3. Database Management (`database.py`)
- Uses Python's built-in `sqlite3` library.
- `init_db()` automatically creates the `candidates` table if it does not already exist with columns: `id`, `name`, `email`, `phone`, `skills`, and `education`.
- `insert_candidate()` uses parameterized SQL queries (`?`) to safely insert candidate records and prevent SQL injection.
- `get_all_candidates()` retrieves all stored records.
- `search_candidates()` performs a `LIKE` search on both candidate names and skills.

### 4. User Interface (`app.py`)
- Built with **Streamlit** to provide a clean web UI without needing HTML, CSS, or JavaScript.
- Divided into two tabs:
  - **Upload & Parse Resume**: Allows file uploading, triggers extraction, and lets the user review/edit extracted information before saving.
  - **View & Search Candidates**: Displays all stored candidates in an interactive data table and includes a real-time search box to filter by name or skill.

---

## 📝 How to Test the Project

1. Open Word or Google Docs and paste the following sample resume text:
   ```text
   Aman Verma
   Email: aman.verma@example.com
   Phone: +91 9876543210
   Education: B.Tech in Computer Science
   
   Technical Skills:
   Python, SQL, HTML, CSS, Git, Machine Learning
   
   Experience:
   Software Engineering Intern at Tech Solutions
   ```
2. Save or Export the document as a **PDF** (`Aman_Verma_Resume.pdf`).
3. In the Streamlit app, upload `Aman_Verma_Resume.pdf`.
4. Click **Extract Details**.
5. Verify the extracted fields and click **Save Candidate to Database**.
6. Switch to the **View & Search Candidates** tab to see the saved record and test searching for "Python" or "Aman".
