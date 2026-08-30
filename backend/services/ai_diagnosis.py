import os, json, urllib.request, urllib.error
from backend.models.troubleshooting import TroubleshootInput, Diagnosis
from backend.services.prompt_service import prompt
def fallback(data: TroubleshootInput, findings):
    failed=[f for f in findings if f.status=='FAIL']
    if failed:
        f=failed[0]; cause=f.message; evidence=[f.evidence]; conf=.88
        command={'Missing route':'show ip route','Trunk configuration issue':'show interfaces trunk','Missing VLAN':'show vlan brief','Interface down/shutdown':'show ip interface brief'}.get(f.rule,'show running-config')
        fix=[f.message+'.','Make the smallest configuration change supported by the evidence.','Retest connectivity; do not apply changes automatically.']
    else:
        cause='More evidence is required to confirm the root cause.'; evidence=['No deterministic rule failure was confirmed from the submitted evidence.']; conf=.42; command='show ip route'; fix=['Collect the recommended command output.','Have a reviewer assess the new evidence before making any change.']
    return Diagnosis(root_cause=cause,confidence=conf,osi_layer='Layer 2' if any(f.rule in ['Missing VLAN','Trunk configuration issue'] for f in failed) else 'Layer 3',evidence=evidence,next_command=command,fix_steps=fix,mode='DEMO_FALLBACK')
def diagnose(data, findings):
    key=os.getenv('LLM_API_KEY'); url=os.getenv('LLM_BASE_URL'); model=os.getenv('LLM_MODEL','gpt-4o-mini')
    if not key or not url: return fallback(data, findings)
    payload={'model':model,'messages':[{'role':'system','content':prompt()},{'role':'user','content':json.dumps({'symptom':data.symptom,'topology_notes':data.topology_notes,'show_outputs':data.show_outputs,'rule_findings':[x.model_dump() for x in findings]})}],'response_format':{'type':'json_object'},'temperature':0}
    request=urllib.request.Request(url.rstrip('/')+'/chat/completions',data=json.dumps(payload).encode(),headers={'Authorization':f'Bearer {key}','Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(request,timeout=30) as response:
            parsed=json.loads(json.loads(response.read())['choices'][0]['message']['content'])
        parsed['mode']='LLM'; return Diagnosis.model_validate(parsed)
    except (urllib.error.URLError,KeyError,ValueError,TypeError) as exc:
        # Do not disguise provider failures: the returned output labels its fallback mode.
        return fallback(data, findings)
