import sqlite3
import pandas as pd
import os

DB_NAME = 'maturity_platform.db'

def init_db():
    """Initialize the SQLite database and create tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Check if we need to migrate schema (simple check)
    try:
        c.execute("SELECT * FROM assessments LIMIT 1")
    except sqlite3.OperationalError:
        pass # Table likely doesn't exist or schema changed

    # Create assessments table
    c.execute('''
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            department TEXT NOT NULL,
            tech_score REAL,
            culture_score REAL,
            process_score REAL,
            skills_score REAL,
            risk_score REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def save_assessment(department, tech, culture, process, skills, risk):
    """Save a single assessment result."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO assessments (department, tech_score, culture_score, process_score, skills_score, risk_score)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (department, tech, culture, process, skills, risk))
    
    conn.commit()
    conn.close()

def load_data():
    """Load all assessment data into a Pandas DataFrame."""
    conn = sqlite3.connect(DB_NAME)
    try:
        df = pd.read_sql_query("SELECT * FROM assessments", conn)
        return df
    except:
        return pd.DataFrame()
    finally:
        conn.close()

def clear_data():
    """Deletes all records from the assessments table."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("DELETE FROM assessments")
        conn.commit()
    except Exception as e:
        print(f"Error clearing data: {e}")
    finally:
        conn.close()

# Initialize on import to ensure DB exists
init_db()