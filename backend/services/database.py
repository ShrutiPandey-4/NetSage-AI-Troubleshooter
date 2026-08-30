import sqlite3, json, os
from pathlib import Path
DB_PATH = Path(os.getenv('NETSAGE_DB', str(Path(__file__).resolve().parents[2] / 'netsage.db')))

def conn():
    c = sqlite3.connect(DB_PATH); c.row_factory = sqlite3.Row; return c
def init_db():
    c=conn()
    c.executescript('''CREATE TABLE IF NOT EXISTS cases(case_id TEXT PRIMARY KEY,symptom TEXT,topology_notes TEXT,show_outputs TEXT,expected_fault TEXT,osi_layer TEXT,concept TEXT,severity TEXT,expected_next_command TEXT,expected_fix TEXT);
    CREATE TABLE IF NOT EXISTS diagnoses(id INTEGER PRIMARY KEY AUTOINCREMENT,case_id TEXT,symptom TEXT,diagnosis_json TEXT,created_at TEXT DEFAULT CURRENT_TIMESTAMP);
    CREATE TABLE IF NOT EXISTS reviews(id INTEGER PRIMARY KEY AUTOINCREMENT,diagnosis_id INTEGER,decision TEXT,correction_json TEXT,final_json TEXT,review_timestamp TEXT DEFAULT CURRENT_TIMESTAMP);
    CREATE TABLE IF NOT EXISTS rule_findings(id INTEGER PRIMARY KEY AUTOINCREMENT,diagnosis_id INTEGER,findings_json TEXT);
    CREATE TABLE IF NOT EXISTS verifications(id INTEGER PRIMARY KEY AUTOINCREMENT,diagnosis_id INTEGER,status TEXT,note TEXT,created_at TEXT DEFAULT CURRENT_TIMESTAMP);''')
    c.commit(); c.close()
def rows(query, args=()):
    c=conn(); out=[dict(x) for x in c.execute(query,args).fetchall()]; c.close(); return out
def execute(query,args=()):
    c=conn(); cur=c.execute(query,args); c.commit(); ident=cur.lastrowid; c.close(); return ident
