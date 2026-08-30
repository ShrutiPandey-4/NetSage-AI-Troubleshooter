import json
from fastapi import APIRouter
from backend.models.troubleshooting import TroubleshootInput
from backend.services.rule_checker import run_checks
from backend.services.ai_diagnosis import diagnose
from backend.services.database import execute
router=APIRouter(prefix='/api',tags=['diagnosis'])
@router.post('/rules/check')
def check(data:TroubleshootInput): return {'findings':[x.model_dump() for x in run_checks(data.show_outputs,data.topology_notes)]}
@router.post('/diagnose')
def diagnose_case(data:TroubleshootInput):
    findings=run_checks(data.show_outputs,data.topology_notes); result=diagnose(data,findings)
    ident=execute('INSERT INTO diagnoses(case_id,symptom,diagnosis_json) VALUES(?,?,?)',(data.case_id,data.symptom,result.model_dump_json()))
    execute('INSERT INTO rule_findings(diagnosis_id,findings_json) VALUES(?,?)',(ident,json.dumps([x.model_dump() for x in findings])))
    return {'diagnosis_id':ident,'diagnosis':result.model_dump(),'rule_findings':[x.model_dump() for x in findings]}
