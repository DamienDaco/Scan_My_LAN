from socket import *
import binascii, struct, sys, re, netifaces


def get_default_interface():
    #Let's get our default interface, by getting the device used by the default IPv4 route.
    default_interface = netifaces.gateways()['default'][netifaces.AF_INET][1]
    return default_interface


def get_mac(interface):

    addrs = netifaces.ifaddresses(interface)
    mac = addrs[netifaces.AF_LINK][0]['addr']
    return mac


def get_host_ip(interface):

    ip = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
    return ip


def get_gateway():

    gateway = netifaces.gateways()['default'][netifaces.AF_INET][0]
    return gateway


def get_interfaces():

    interface_list = netifaces.interfaces()
    return interface_list


def hex_mac(mac):

    cleanmac = re.findall('[a-fA-F0-9]{2}', mac)
    hexmac = [int(i, 16) for i in cleanmac]
    return hexmac


def decimal_ip(ip):

    cleanip = re.findall('\d{1,3}', ip)
    decimalip = [int(i) for i in cleanip]
    return decimalip


def build_arp_query(source_mac, source_ip, dest_ip):

    broadcast_mac = [0xFF] * 6
    arp_frame = struct.pack('!6B6BH', *[*broadcast_mac, *source_mac, 0x0806])
    arp_packet = struct.pack('!HHBBH6B4B6B4B', *[0x0001, 0x0800, 0x06, 0x04, 0x0001, *source_mac, *source_ip, *broadcast_mac, *dest_ip])
    arp_query = arp_frame + arp_packet

    return arp_query


def send_data(iface, data):

    s = socket(AF_PACKET, SOCK_RAW)
    s.bind((iface, 0))
    s.send(data)


