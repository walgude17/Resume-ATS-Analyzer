from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from pypdf import PdfReader
import sqlite3
import os
import json 

app = FastAPI(title="Resume Analyzer API")

DATABASE_NAME = "resume_analyzer.db"

TARGET_SKILLS = [
  "python",
  "fastapi",
  "sql",
  "django",
  "aws",
  "docker",
  "javascript",
  "react"
]

@app.get("/")
def home():
  return {
    "message": "Resume Analyzer API is running",
    "status": "active"
  }

@app.post("/analyze-resume/")  
async def analyze_resume(
  name: str = Form(...),
  email: str = Form(...),
  target_role: str = Form(...),
  file: UploadFile = File(...)
  ):

#Check PDF
  if not file.filename.lower().endswith(".pdf"):
    raise HTTPException(
      status_code=400,
      detail="Only PDF files are allowed")

#Save the uploaded PDF temporarily
  upload_dir = "uploaded_files"
  os.makedirs(upload_dir, exist_ok=True)

  file_path = os.path.join(upload_dir,file.filename) 
  
  try:
    content = await file.read()
    
    with open(file_path,"wb") as f:
      f.write(content)

    reader = PdfReader(file_path)

    extracted_text = ""  

    for page in reader.pages:
      text = page.extract_text()

      if text :
        extracted_text += text.lower() + ""

    matched_skills = [
      skill for skill in TARGET_SKILLS
      if skill in extracted_text
      ] 

    missing_skills = [
      skill for skill in TARGET_SKILLS
      if skill not in matched_skills
    ]  
    #calculate score
    ats_score = round((len(matched_skills)/len(TARGET_SKILLS)) * 100,2) if TARGET_SKILLS else 0.0
    #Database connection
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO candidates (name, email, filename) VALUES (?,?,?)",
     (name, email, file.filename))
    candidate_id = cursor.lastrowid

    #insert analysis result
    cursor.execute("INSERT INTO analysis_results(candidate_id,target_role,ats_score,matched_skills,missing_skills) VALUES (?,?,?,?,?)",
                  (candidate_id,target_role,ats_score,json.dumps(matched_skills),json.dumps(missing_skills)))

    conn.commit()
    conn.close()

    return {
      "candidate_id":candidate_id,
      "name":name,
      "email":email,
      "filename":file.filename,
      "target_role":target_role,
      "ats_score":ats_score,
      "matched_skills":matched_skills,
      "missing_skills":missing_skills,
      "status":"Resume analyzed sucessfully"

    }
  except  Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
    
  finally:
      #Delete temporary PDF
      if os.path.exists(file_path):
        os.remove(file_path)