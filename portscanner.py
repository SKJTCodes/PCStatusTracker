import nmap
import traceback
from scapy.all import ARP, Ether, srp

class Scanner():
  def __init__(self, net_add, log, type="nmap") -> None:
    self.log = log
    self.type = type
    if self.type == "nmap":
      self._init_nmap(net_add)
    elif self.type == "scapy":
      self._init_scapy(net_add)
  
  def _init_scapy(self, net_add):
    arp = ARP(pdst=net_add)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    self.packet = ether/arp
  
  def _init_nmap(self, net_add, args="-sn"):
    nm = nmap.PortScanner()
    self.scan_results = nm.scan(hosts=net_add, arguments=args)

  def get_results(self):
    if self.type == 'nmap':
      self.results = self._nmap_results()
    elif self.type == "scapy":
      self.results = self._scapy_results()
    else:
      self.log.error(f"Type does not exist: {self.type}")
      return []
    
    return self.results

  def print_debug(self, fmt='{:16}\t{}'):
    self.log.info(fmt.format("IP", "MAC"))
    for result in self.results:
      self.log.info(fmt.format(result['ip'], result['mac']))

  def _scapy_results(self):
    results = srp(self.packet, timeout=3, verbose=0)[0]
    clients = []
    for sent, received in results:
      clients.append({'ip': received.psrc, 'mac': received.hwsrc.upper(), 'state': None})

    return clients

  def _nmap_results(self):
    """
    Once in awhile, it generates an error but sometimes it doesnt.
    nmap.nmap.PortScannerError: "nmap: Target.cc:503: void Target::stopTimeOutClock(const timeval*): Assertion `htn.toclock_running == true' failed.\n"

    """
    data = []
    for ip, item in self.scan_results['scan'].items():
      if item['status']['reason'] == 'localhost-response':
        data.append({'ip': ip, 'mac': 'local', 'state': item['status']['state']})
        continue  
      try:
        data.append({'ip': ip, 'mac': item['addresses']['mac'].upper(), 'state': item['status']['state']})
      except KeyError:
        e = traceback.format_exc()
        self.log.error(e)
        self.log.error(item)
    return data

# from Logger import Log
# import os
# logs = Log(os.getcwd())
# scan = Scanner(net_add="192.168.68.0/24", log=logs.get_logger(), type="scapy")
# scan.get_results()
