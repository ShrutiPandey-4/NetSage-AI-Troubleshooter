from backend.services.rule_checker import run_checks
def status(text,rule): return next(x.status for x in run_checks(text) if x.rule==rule)
def test_duplicate_ip(): assert status('PC A ip address 10.1.1.2 PC B ip address 10.1.1.2','Duplicate IP')=='FAIL'
def test_mask(): assert status('ip address 192.168.1.2 255.255.0.0 /24','Wrong subnet mask')=='FAIL'
def test_gateway(): assert status('default gateway mismatch different subnet','Gateway mismatch')=='FAIL'
def test_down(): assert status('interface Fast0/1 administratively down down','Interface down/shutdown')=='FAIL'
def test_vlan(): assert status('vlan 30 missing','Missing VLAN')=='FAIL'
def test_route(): assert status('network 10.2.0.0 not in table','Missing route')=='FAIL'
def test_trunk(): assert status('show interfaces trunk: Gi0/1 trunking off','Trunk configuration issue')=='FAIL'
