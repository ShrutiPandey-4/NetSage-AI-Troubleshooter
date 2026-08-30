from fastapi import APIRouter
from backend.services.database import rows
router=APIRouter(prefix='/api/dashboard',tags=['dashboard'])
@router.get('/stats')
def stats():
    total=rows('SELECT COUNT(*) n FROM cases')[0]['n']; concepts=rows('SELECT concept,COUNT(*) count FROM cases GROUP BY concept'); severity=rows('SELECT severity,COUNT(*) count FROM cases GROUP BY severity'); decisions=rows('SELECT decision,COUNT(*) count FROM reviews GROUP BY decision'); reviewed=sum(x['count'] for x in decisions); accepted=next((x['count'] for x in decisions if x['decision']=='ACCEPTED'),0)
    return {'total_cases':total,'concepts':concepts,'severity':severity,'decisions':decisions,'agreement_rate':accepted/reviewed if reviewed else 0,'reviewed':reviewed}
