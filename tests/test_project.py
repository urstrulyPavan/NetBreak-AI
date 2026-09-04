from core.challenge_engine import load_challenges
from core.simulator import NetworkSimulator
from pathlib import Path

def test_30_scenarios():
    c=load_challenges()
    assert len(c)==30
    assert sum(x.difficulty=="Beginner" for x in c)==15
    assert sum(x.difficulty=="Intermediate" for x in c)==15

def test_route():
    c=next(x for x in load_challenges() if x.id=="route_01")
    s=NetworkSimulator(c)
    assert "NOT present" in s.run("show ip route").output
    s.run("ip route 10.10.20.0 255.255.255.0 192.168.2.2")
    assert "100 percent" in s.run("ping 10.10.20.10").output

def test_vlan():
    c=next(x for x in load_challenges() if x.id=="vlan_01")
    s=NetworkSimulator(c)
    s.run("switchport access vlan 10")
    assert s.state.fixed

def test_no_env_file():
    assert not Path(".env").exists()
