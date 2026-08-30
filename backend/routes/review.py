import json
from fastapi import APIRouter,HTTPException
from backend.models.troubleshooting import ReviewInput,VerificationInput
from backend.services.database import execute,rows
router=APIRouter(prefix='/api',tags=['review'])
@router.post('/reviews')
def review(x:ReviewInput):
    d=rows('SELECT diagnosis_json FROM diagnoses WHERE id=?',(x.diagnosis_id,))
    if not d: raise HTTPException(404,'Diagnosis not found')
    ai=json.loads(d[0]['diagnosis_json']); final=x.correction.model_dump() if x.correction else ai
    ident=execute('INSERT INTO reviews(diagnosis_id,decision,correction_json,final_json) VALUES(?,?,?,?)',(x.diagnosis_id,x.decision,json.dumps(x.correction.model_dump() if x.correction else None),json.dumps(final)))
    return {'review_id':ident,'final_diagnosis':final}
@router.get('/reviews')
def reviews(decision:str|None=None):
    q='SELECT r.*,d.case_id,d.diagnosis_json FROM reviews r JOIN diagnoses d ON d.id=r.diagnosis_id'; return rows(q+(' WHERE r.decision=?' if decision else '')+' ORDER BY r.review_timestamp DESC',(decision,) if decision else ())
@router.post('/verification')
def verify(x:VerificationInput):
    if not rows('SELECT id FROM reviews WHERE diagnosis_id=?',(x.diagnosis_id,)): raise HTTPException(400,'Human review is required before verification')
    return {'verification_id':execute('INSERT INTO verifications(diagnosis_id,status,note) VALUES(?,?,?)',(x.diagnosis_id,x.status,x.note))}
