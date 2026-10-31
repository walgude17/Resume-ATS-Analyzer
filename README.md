# Rule-Based Resume ATS Analyzer

A high-performance backend REST API built with **FastAPI** that parses candidate resumes (PDFs), extracts text structure, computes an automated ATS match score based on targeted skills matrices, and stores persistent transactional logs in a relational database layout.

## 🚀 Key Architectural Features
- **Asynchronous Multipart Processing:** Handles concurrent multi-part form data uploads natively using FastAPI async loops.
- **Dynamic Text Processing:** Extracts text data layers page-by-page utilizing the `pypdf` library extraction pipelines.
- **Relational Data Mapping:** Integrates an `sqlite3` data architecture linking independent `candidates` identity profiles to persistent analytical `analysis_results` records via Foreign Keys.
- **Automatic Documentation:** Built-in OpenAPI Swagger UI console panel available out-of-the-box for instant testing.

## 🛠️ Technology Stack
- **Backend Framework:** Python, FastAPI, Uvicorn
- **Data Parsing Engine:** PyPDF (`PdfReader`)
- **Database Engine:** SQLite (Relational Schema)

## 🔧 Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd resume-analyzer
   ```

2. **Install the dependencies:**
   ```bash
   pip install fastapi uvicorn pypdf
   ```

3. **Start the Uvicorn local development server:**
   ```bash
   python -m uvicorn main:app --reload
   ```

4. **Access the Interactive API Testing UI:**
   Open your web browser and navigate to: `http://127.0.0`

## 📊 Endpoints Implemented
- `GET /` - Health check route confirming live server activity status.
- `POST /analyze-resume/` - Main ingestion endpoint taking name, email, target_role, and raw multipart file strings. Extracts vocabulary assets, logs rows across tables, and provides JSON metrics detailing match breakdowns and calculated percentages.
-