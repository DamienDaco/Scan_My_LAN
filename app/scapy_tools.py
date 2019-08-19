from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
from scapy.all import *


class ScapyArpSnifferWorker(QObject):
    send_list_signal = pyqtSignal(list)
    finished = pyqtSignal(name="done")

    def __init__(self, live_hosts):
        super().__init__()
        self.live_hosts = live_hosts
        print("Received list: {}".format(self.live_hosts))

    @pyqtSlot()
    def task(self):

        def arp_display(pkt):
            if pkt[0][1].op == 1:
                print("{} with MAC {} is asking where {} is".format(pkt[ARP].psrc, pkt[ARP].hwsrc, pkt[ARP].pdst))
            elif pkt[0][1].op == 2:
                print("{} is at {}".format(pkt[ARP].psrc, pkt[ARP].hwsrc))
            host_dict = {
                "IP Address": pkt[ARP].psrc,
                "MAC Address": pkt[ARP].hwsrc
            }
            # Check if IP Address is in our list:
            # Also eliminate the special '0.0.0.0' case (Host without IP address yet):
            if not any(d.get('IP Address') == pkt[ARP].psrc or (pkt[ARP].psrc == '0.0.0.0') for d in self.live_hosts):
                self.live_hosts.append(host_dict)
                print(self.live_hosts)
                self.send_list_signal.emit(self.live_hosts)

            # If an IP Address has been allocated to another host, update the MAC address:
            elif any(d.get('IP Address') == pkt[ARP].psrc and not d.get('MAC Address') == pkt[ARP].hwsrc for d in
                     self.live_hosts):
                for d in self.live_hosts:
                    if d['IP Address'] == pkt[ARP].psrc:
                        d['MAC Address'] = pkt[ARP].hwsrc
                print("Host {} updated with new MAC Address {}".format(pkt[ARP].psrc, pkt[ARP].hwsrc))
                print(self.live_hosts)
                self.send_list_signal.emit(self.live_hosts)

        print(sniff(prn=arp_display, filter="arp"))
        print(self.live_hosts)
        self.send_list_signal.emit(self.live_hosts)
