import sqlite3
import json

DATABASE_NAME="resume_analyzer.db"

def init_db():
#Intialize the database and create relational table with raw SQL.

   conn = sqlite3.connect(DATABASE_NAME)
   cursor = conn.cursor()

#Unable foreign key support in SQLite
   cursor.execute("PRAGMA foreign_keys = ON;")

## 1. Create parent table = candidates
   cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         name TEXT,
         email TEXT,
         filename TEXT NOT NULL
         );  
         """)

## 2. Create child table = analysis_results

   cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis_results(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         candidate_id INTEGER,
         target_role TEXT NOT NULL,
         ats_score REAL NOT NULL,
         matched_skills TEXT,
         missing_skills TEXT,
         evaluation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
         FOREIGN KEY(candidates_id) REFERENCES candidates(id) ON DELETE CASCADE
         );
         """)
  
   conn.commit()
   conn.close()      
print("Datebase successfully initializes using Pure SQL Queries!")

if __name__ == "__main__":
  init_db()
