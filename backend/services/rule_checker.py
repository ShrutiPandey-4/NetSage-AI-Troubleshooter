import re
from backend.models.troubleshooting import RuleFinding
def finding(rule,status,severity,evidence,message): return RuleFinding(rule=rule,status=status,severity=severity,evidence=evidence,message=message)
def run_checks(show_outputs: str, topology_notes: str=''):
    text=(show_outputs+'\n'+topology_notes).lower(); out=[]
    ips=re.findall(r'(?:ip address\s+|\b)(\d{1,3}(?:\.\d{1,3}){3})', text)
    duplicates={x for x in ips if ips.count(x)>1 and x!='0.0.0.0'}
    out.append(finding('Duplicate IP','FAIL' if duplicates else ('PASS' if ips else 'INSUFFICIENT_EVIDENCE'),'high' if duplicates else 'low', ', '.join(duplicates) or 'No repeated address found' if ips else 'No IP addresses supplied','Duplicate address detected' if duplicates else 'No duplicate address detected' if ips else 'Need interface or host addressing output'))
    mask_bad=bool(re.search(r'(255\.255\.0\.0|255\.0\.0\.0)',text) and re.search(r'/24|255\.255\.255\.0',text))
    out.append(finding('Wrong subnet mask','FAIL' if mask_bad else ('INSUFFICIENT_EVIDENCE' if not ips else 'PASS'),'medium','Conflicting /24 and broader masks' if mask_bad else 'Addressing details unavailable' if not ips else 'No conflicting mask seen','Subnet mask conflicts with stated LAN' if mask_bad else 'No mismatch detected' if ips else 'Need host IP/mask and gateway'))
    gw_bad='default gateway' in text and ('mismatch' in text or 'different subnet' in text)
    out.append(finding('Gateway mismatch','FAIL' if gw_bad else ('INSUFFICIENT_EVIDENCE' if 'gateway' not in text else 'PASS'),'high','Gateway mismatch marker' if gw_bad else 'Gateway not supplied' if 'gateway' not in text else 'No mismatch marker','Host gateway is outside its subnet' if gw_bad else 'No gateway mismatch detected' if 'gateway' in text else 'Need host gateway evidence'))
    down=bool(re.search(r'\b(administratively down|shutdown)\b',text))
    out.append(finding('Interface down/shutdown','FAIL' if down else ('PASS' if 'interface' in text else 'INSUFFICIENT_EVIDENCE'),'high','Administrative down/shutdown present' if down else 'No interface state supplied' if 'interface' not in text else 'No shutdown state found','Enable the affected interface' if down else 'No shutdown detected' if 'interface' in text else 'Run show ip interface brief'))
    vlan_missing=bool(re.search(r'vlan\s+(?:30|[0-9]+).*?(?:missing|not active|does not exist)',text))
    out.append(finding('Missing VLAN','FAIL' if vlan_missing else ('PASS' if 'vlan' in text else 'INSUFFICIENT_EVIDENCE'),'medium','VLAN missing/not active' if vlan_missing else 'No VLAN data' if 'vlan' not in text else 'No missing VLAN evidence','Create/activate the required VLAN' if vlan_missing else 'No missing VLAN detected' if 'vlan' in text else 'Run show vlan brief'))
    route_missing=bool(re.search(r'(network .*not in table|no route|gateway of last resort is not set)',text))
    out.append(finding('Missing route','FAIL' if route_missing else ('PASS' if 'route' in text else 'INSUFFICIENT_EVIDENCE'),'high','Route absence reported' if route_missing else 'No routing table data' if 'route' not in text else 'No absent route marker','Add or learn a route to the destination' if route_missing else 'No missing route detected' if 'route' in text else 'Run show ip route'))
    trunk_bad=bool(re.search(r'(trunking.*(?:off|not-trunking)|native vlan mismatch|allowed vlan.*(?:not|exclude))',text))
    out.append(finding('Trunk configuration issue','FAIL' if trunk_bad else ('PASS' if 'trunk' in text else 'INSUFFICIENT_EVIDENCE'),'medium','Trunk mismatch/disabled evidence' if trunk_bad else 'No trunk data' if 'trunk' not in text else 'No trunk issue marker','Correct trunk mode/native/allowed VLANs' if trunk_bad else 'No trunk issue detected' if 'trunk' in text else 'Run show interfaces trunk'))
    return out
