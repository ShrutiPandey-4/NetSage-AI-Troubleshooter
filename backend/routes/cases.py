from fastapi import APIRouter, HTTPException
from backend.services.database import rows
router=APIRouter(prefix='/api/cases',tags=['cases'])
@router.get('')
def all_cases(): return rows('SELECT * FROM cases ORDER BY case_id')
@router.get('/{case_id}')
def one_case(case_id:str):
    found=rows('SELECT * FROM cases WHERE case_id=?',(case_id,))
    if not found: raise HTTPException(404,'Case not found')
    return found[0]
