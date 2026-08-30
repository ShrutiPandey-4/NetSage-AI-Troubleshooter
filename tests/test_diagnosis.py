from backend.models.troubleshooting import TroubleshootInput
from backend.services.ai_diagnosis import diagnose
from backend.services.rule_checker import run_checks
def test_diagnosis_schema():
 x=TroubleshootInput(symptom='host cannot connect',show_outputs='interface administratively down down')
 d=diagnose(x,run_checks(x.show_outputs)); assert 0<=d.confidence<=1 and d.evidence and d.mode=='DEMO_FALLBACK'
