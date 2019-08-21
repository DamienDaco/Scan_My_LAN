from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from scapy.all import *
from app.network_functions import *


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
            # host_dict = [[
            #     pkt[ARP].psrc,
            #     pkt[ARP].hwsrc
            # ]]
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


class ScapyArpQueryWorker(QObject):
    str_signal = pyqtSignal(str)
    finished = pyqtSignal(name="done")

    def __init__(self, iface, first_ip,last_ip):
        super().__init__()
        self.iface = iface
        self.first_ip = first_ip
        self.last_ip = last_ip
        self._is_running = True

    @pyqtSlot()
    def stop_worker(self):
        print("Worker received the Stop signal")
        self._is_running = False
        print("_is_running is {}".format(self._is_running))

    @pyqtSlot()
    def task(self):

        for i in range(self.first_ip, self.last_ip + 1):
            dotted_ip = integer_to_dotted_decimal_ip(i)
            print("Sending packet to", dotted_ip)
            self.str_signal.emit(dotted_ip)
            pkt = scapy.sendp(scapy.Ether(dst="ff:ff:ff:ff:ff:ff")/scapy.ARP(pdst=dotted_ip), verbose=True)
            # if pkt[0][0][1]:
            #     print("{} is at {}".format(dotted_ip, pkt[0][0][1].hwsrc))
            QThread.msleep(10)
            QApplication.processEvents()
            if not self._is_running:
                break

        self._is_running = False
        self.finished.emit()
