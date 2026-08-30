import csv
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.services.database import init_db,conn
from backend.routes import cases,diagnosis,review,dashboard
app=FastAPI(title='NetSage AI')
app.add_middleware(CORSMiddleware,allow_origins=['http://localhost:5173'],allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
@app.on_event('startup')
def startup():
 init_db(); c=conn();
 if not c.execute('SELECT 1 FROM cases LIMIT 1').fetchone():
  with open(Path(__file__).resolve().parents[1]/'data'/'cases.csv',newline='',encoding='utf-8') as f:
   for r in csv.DictReader(f): c.execute('INSERT INTO cases VALUES (:case_id,:symptom,:topology_notes,:show_outputs,:expected_fault,:osi_layer,:concept,:severity,:expected_next_command,:expected_fix)',r)
  c.commit()
 c.close()
app.include_router(cases.router); app.include_router(diagnosis.router); app.include_router(review.router); app.include_router(dashboard.router)
@app.get('/health')
def health(): return {'status':'ok','ai_mode':'LLM when configured; otherwise explicit DEMO_FALLBACK'}
