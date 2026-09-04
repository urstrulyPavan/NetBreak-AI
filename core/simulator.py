from dataclasses import dataclass, field
from models import Challenge, CommandResult

FIXES = {
"ip_01":"no shutdown","ip_02":"192.168.1.1","ip_03":"192.168.1.11","ip_04":"255.255.255.0","ip_05":"no shutdown",
"vlan_01":"switchport access vlan 10","vlan_02":"vlan 30","vlan_03":"allowed vlan 10","route_01":"ip route 10.10.20.0",
"route_02":"192.168.2.2","route_03":"0.0.0.0 0.0.0.0","int_01":"192.168.2.1","dhcp_01":"ip helper-address",
"dns_01":"10.10.20.53","mix_01":"vlan 10","acl_01":"no access-list 100","acl_02":"permit icmp","acl_03":"remove deny",
"acl_04":"no ip access-group","vlan_04":"native vlan 1","vlan_05":"allowed vlan 30","route_04":"administrative distance",
"route_05":"192.168.2.2","route_06":"192.168.2.2","int_02":"duplex auto","dhcp_02":"expand pool",
"dhcp_03":"default-router 192.168.1.1","dns_02":"10.10.20.10","mix_02":"ip route 10.10.20.0","mix_03":"no shutdown",
"mix_04":"switchport access vlan 30","mix_05":"ip helper-address","mix_06":"permit udp 53","mix_07":"10.0.1.1"
}

@dataclass
class NetworkState:
    fixed: bool=False
    secondary_fixed: bool=False
    command_history: list[str]=field(default_factory=list)

class NetworkSimulator:
    def __init__(self, challenge: Challenge):
        self.challenge=challenge
        self.state=NetworkState()
        self.history=[]

    def run(self, raw):
        cmd=" ".join(raw.strip().lower().split())
        self.state.command_history.append(cmd)
        if not cmd: return self._result(raw,"% Please enter a command.",False)
        fix=FIXES.get(self.challenge.id,"")
        if fix and fix in cmd:
            if self.challenge.id=="mix_01" and "vlan 10" in cmd:
                self.state.secondary_fixed=True
            elif self.challenge.id=="mix_01" and "192.168.1.1" in cmd:
                self.state.secondary_fixed=True
            else:
                self.state.fixed=True
            return self._result(raw,"Configuration change applied.",changed_state=True)
        if cmd in ("help","?"): return self._result(raw,self.help())
        if cmd=="show ip interface brief": return self._result(raw,self.interfaces())
        if cmd.startswith("show interfaces") and "switchport" in cmd: return self._result(raw,self.switchport())
        if cmd.startswith("show interfaces") and "status" in cmd: return self._result(raw,self.port_status())
        if cmd=="show vlan brief": return self._result(raw,self.vlan())
        if cmd in ("show interfaces trunk","show interface trunk"): return self._result(raw,self.trunk())
        if cmd=="show ip route": return self._result(raw,self.route())
        if cmd in ("show access-lists","show ip access-lists"): return self._result(raw,self.acl())
        if cmd in ("show running-config","show run"): return self._result(raw,self.run_config())
        if cmd in ("show ip interface","show interfaces"): return self._result(raw,self.run_config())
        if cmd in ("show ip dhcp pool","show ip dhcp binding"): return self._result(raw,self.dhcp())
        if cmd in ("ipconfig","ipconfig /all"): return self._result(raw,self.ipconfig())
        if cmd.startswith("nslookup "): return self._result(raw,self.nslookup())
        if cmd.startswith("traceroute "): return self._result(raw,self.traceroute())
        if cmd.startswith("ping "): return self.ping(cmd)
        return self._result(raw,"% Invalid input. Type 'help'.",False)

    def interfaces(self):
        c=self.challenge.id
        if c=="ip_01" and not self.state.fixed: return "Interface  IP-Address  Status                 Protocol\nG0/0       192.168.1.1 administratively down    down"
        if c=="int_01" and not self.state.fixed: return "Interface  IP-Address  Status  Protocol\nG0/1       192.168.3.1  up      up"
        if c=="mix_03" and not self.state.fixed: return "Interface  IP-Address  Status                 Protocol\nG0/1       192.168.2.1 administratively down    down"
        if c=="mix_07" and not self.state.fixed: return "Interface  IP-Address  Status  Protocol\nG0/1       10.0.0.1     up      up"
        return "Interface  IP-Address  Status  Protocol\nG0/0       192.168.1.1 up      up"

    def port_status(self):
        return "Port   Status\nFa0/1  connected" if self.state.fixed else "Port   Status\nFa0/1  down"

    def switchport(self):
        if self.challenge.id=="vlan_01" and not self.state.fixed: v="20"
        elif self.challenge.id=="mix_04" and not self.state.fixed: v="40"
        else: v="10"
        return f"Name: Fa0/1\nAdministrative Mode: static access\nAccess Mode VLAN: {v}"

    def vlan(self):
        if self.challenge.id=="vlan_02" and not self.state.fixed: return "VLAN 10 USERS active\nVLAN 20 SERVERS active\nVLAN 30 missing"
        if self.challenge.id=="vlan_01" and not self.state.fixed: return "VLAN 10 USERS active Fa0/2\nVLAN 20 SERVERS active Fa0/1"
        if self.challenge.id=="mix_04" and not self.state.fixed: return "VLAN 30 USERS active\nVLAN 40 GUESTS active Fa0/1"
        return "VLAN 10 USERS active Fa0/1,Fa0/2\nVLAN 20 SERVERS active"

    def trunk(self):
        c=self.challenge.id
        if c=="vlan_03" and not self.state.fixed: return "Port Gi0/1 trunking\nNative VLAN: 1\nVLANs allowed: 1,20"
        if c=="vlan_04" and not self.state.fixed: return "Port Gi0/1 trunking\nNative VLAN: 99"
        if c=="vlan_05" and not self.state.fixed: return "Port Gi0/1 trunking\nVLANs allowed: 1,40"
        return "Port Gi0/1 trunking\nNative VLAN: 1\nVLANs allowed: 1,10,20,30"

    def route(self):
        c=self.challenge.id
        if c in ("route_01","mix_02") and not self.state.fixed: return "C 192.168.1.0/24 connected\n!! 10.10.20.0/24 NOT present"
        if c=="route_02" and not self.state.fixed: return "S 10.10.20.0/24 [1/0] via 192.168.2.99"
        if c=="route_03" and not self.state.fixed: return "Gateway of last resort is not set"
        if c=="route_04" and not self.state.fixed: return "S 10.10.20.0/24 [200/0] via 192.168.2.2\nO 10.10.20.0/24 [110/20] via 192.168.3.2"
        if c=="route_05" and not self.state.fixed: return "S 10.10.20.0/24 [1/0] via 192.168.3.2"
        if c=="route_06" and not self.state.fixed: return "S 10.10.20.0/24 [1/0] via 192.168.99.2"
        return "S 10.10.20.0/24 [1/0] via 192.168.2.2"

    def acl(self):
        c=self.challenge.id
        if c=="acl_01" and not self.state.fixed: return "Extended ACL 100\n10 deny ip 192.168.1.0 0.0.0.255 10.10.20.0 0.0.0.255\n20 permit ip any any"
        if c=="acl_02" and not self.state.fixed: return "Extended ACL 100\n10 deny icmp 192.168.1.0 0.0.0.255 any\n20 permit ip any any"
        if c=="acl_03" and not self.state.fixed: return "Extended ACL 100\n10 deny ip any any\n20 permit ip 192.168.1.0 0.0.0.255 10.10.20.0 0.0.0.255"
        if c=="mix_06" and not self.state.fixed: return "Extended ACL 120\n10 deny udp any host 10.10.20.53 eq 53\n20 permit ip any any"
        return "Extended ACL 100\n10 permit ip any any"

    def run_config(self):
        c=self.challenge.id
        if c=="ip_02" and not self.state.fixed: return "PC1 IP: 192.168.1.10/24\nDefault gateway: 192.168.2.1"
        if c=="ip_04" and not self.state.fixed: return "PC1 IP: 192.168.1.10\nSubnet Mask: 255.255.255.252"
        if c in ("dhcp_01","mix_05") and not self.state.fixed: return "interface G0/0\n! no ip helper-address configured"
        if c=="dhcp_03" and not self.state.fixed: return "ip dhcp pool USERS\ndefault-router 192.168.2.1"
        return "interface G0/0\nip address 192.168.1.1 255.255.255.0"

    def dhcp(self):
        if self.challenge.id=="dhcp_02" and not self.state.fixed: return "Pool USERS\nAddresses available: 0\nStatus: EXHAUSTED"
        return "Pool USERS\nAddresses available: 20\nStatus: ACTIVE"

    def ipconfig(self):
        c=self.challenge.id
        if c=="dhcp_01" and not self.state.fixed: return "IPv4: 169.254.10.20\nGateway: 0.0.0.0"
        if c=="dhcp_03" and not self.state.fixed: return "IPv4: 192.168.1.20\nGateway: 192.168.2.1"
        if c=="dns_01" and not self.state.fixed: return "IPv4: 192.168.1.10\nGateway: 192.168.1.1\nDNS: 8.8.8.8"
        return "IPv4: 192.168.1.10\nGateway: 192.168.1.1"

    def nslookup(self):
        if self.challenge.id=="dns_01" and not self.state.fixed: return "Server: 8.8.8.8\n*** Request timed out"
        if self.challenge.id=="dns_02" and not self.state.fixed: return "Name: server.example.local\nAddress: 10.10.20.9"
        if self.challenge.id=="mix_06" and not self.state.fixed: return "*** DNS request timed out"
        return "Name: server.example.local\nAddress: 10.10.20.10"

    def traceroute(self):
        if self.challenge.id=="route_05" and not self.state.fixed: return "1 192.168.2.2\n2 192.168.3.2\n3 192.168.2.2\n... loop detected"
        return "1 192.168.1.1\n2 192.168.2.2\n3 10.10.20.10"

    def ping(self,cmd):
        target=cmd.split(maxsplit=1)[1] if len(cmd.split())>1 else ""
        c=self.challenge.id
        ok=self.state.fixed
        if c=="dns_01" and target=="10.10.20.10": ok=True
        if target=="192.168.1.1" and c not in ("ip_01","ip_02","mix_01"): ok=True
        if c=="mix_01": ok=self.state.fixed and self.state.secondary_fixed
        if c in ("vlan_01","vlan_03","vlan_04","vlan_05","mix_04"): ok=self.state.fixed
        return self._result(cmd,f"Sending 5 ICMP Echos to {target}...\\n{'!!!!!' if ok else '.....'}\\nSuccess rate is {'100' if ok else '0'} percent ({'5/5' if ok else '0/5'})")

    def verify(self):
        return self.state.fixed

    def help(self):
        return "show ip interface brief | show ip route | show vlan brief | show interfaces trunk | show access-lists | show running-config | show ip dhcp pool | ipconfig /all | ping <ip> | traceroute <ip> | nslookup <hostname>"

    def _result(self,command,output,success=True,changed_state=False):
        r=CommandResult(command=command,output=output,success=success,changed_state=changed_state)
        self.history.append(r); return r
