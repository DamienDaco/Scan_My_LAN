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


def get_host_mask(interface):

    mask = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']
    return mask


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


def integer_to_dotted_decimal_ip(i):

    i = '{0:032b}'.format(i)
    decimal_ip = '.'.join(map(str, [int(i[:8], 2), int(i[8:16], 2), int(i[16:24], 2), int(i[24:32], 2)]))
    return decimal_ip


def calc_range(ip, mask):

    broadcast = 0b11111111111111111111111111111111               # This is the equivalent of 255.255.255.255

    octets_ip = [int(i) for i in ip.split('.')]
    string_ip = '{0:08b}{1:08b}{2:08b}{3:08b}'.format(*octets_ip)
    int_ip = int(string_ip, 2)
    octets_mask = [int(i) for i in mask.split('.')]
    string_mask = '{0:08b}{1:08b}{2:08b}{3:08b}'.format(*octets_mask)
    int_mask = int(string_mask, 2)
    host_bits = bin(broadcast ^ int(string_mask, 2)).count('1')
    '''
    Explanation on the previous line of code:
    We have to perform an XOR operation with '^' to compute the number of host bits (The zeroes on the right of a network mask)
    bin() returns a string like '0b11111111'
    Len() will tell us the length of that string
    We have to substract 2 because bin() prepends two chars '0b' before our string  
    '''

    print("Number of host bits: %d" % host_bits)

    if host_bits > 1:
        int_subnet_id = int_ip & int_mask
        int_first_ip = int_subnet_id + 1
        int_broadcast_ip = broadcast ^ int_mask | int_ip
        int_last_ip = int_broadcast_ip - 1

        dotted_id, dotted_first_ip, dotted_last_ip, dotted_broadcast = map(
            integer_to_dotted_decimal_ip, [int_subnet_id, int_first_ip, int_last_ip, int_broadcast_ip])

        print("Your network ID is %s" % dotted_id)
        print("Your first IP is %s" % dotted_first_ip)
        print("Your last IP is %s" % dotted_last_ip)
        print("Your broadcast is %s" % dotted_broadcast)

        return int_first_ip, int_last_ip

    if host_bits == 1:                                          # This is a very special case for /31 networks (e.g. Cisco routers). Probably useless but whatever?
        int_first_ip = int_ip & int_mask
        int_last_ip = int_first_ip + 1

        dotted_first_ip, dotted_last_ip = map(integer_to_dotted_decimal_ip, [int_first_ip, int_last_ip])
        print("Your first IP is %s" % dotted_first_ip)
        print("Your last IP is %s" % dotted_last_ip)

    if host_bits == 0:                                          # Another special case for /32 'networks'. Probably useless.
        dotted_first_ip = integer_to_dotted_decimal_ip(int_ip)

        print("Your IP is %s" % dotted_first_ip)


def build_arp_query(source_mac, source_ip, dest_ip):

    broadcast_mac = [0xFF] * 6
    arp_frame = struct.pack('!6B6BH', *[*broadcast_mac, *source_mac, 0x0806])
    arp_packet = struct.pack('!HHBBH6B4B6BL', *[0x0001, 0x0800, 0x06, 0x04, 0x0001, *source_mac, *source_ip, *broadcast_mac, dest_ip])
    arp_query = arp_frame + arp_packet

    return arp_query


def send_data(iface, data):

    s = socket(AF_PACKET, SOCK_RAW)
    s.bind((iface, 0))
    s.send(data)


def sniff_arp(interface, host_list):
    s = socket(AF_PACKET, SOCK_RAW, htons(0x0806))

    # print("Capturing ARP replies on interface {}".format(interface))
    s.bind((interface, 0))

    try:
        datagram = s.recvfrom(2048)

        ethernet_header = datagram[0][0:14]
        ethernet_unpacked = struct.unpack("!6s6s2s", ethernet_header)

        arp_header = datagram[0][14:42]
        arp_unpacked = struct.unpack("!2s2s1s1s2s6s4s6s4s", arp_header)

        ip = inet_ntoa(arp_unpacked[6])
        # Check for ARP replies only (code is 0x0002, or b'0002' in binary output
        # if binascii.hexlify(arp_unpacked[4]) == b'0002':
            # Check if the ip is already in our list:
        if ip not in (i[0] for i in host_list):
            print("inet_ntoa(arp_unpacked[6] is", inet_ntoa(arp_unpacked[6]))
            remote_mac = binascii.hexlify(ethernet_unpacked[1])
            decoded_mac = remote_mac.decode()
            human_mac = ':'.join(decoded_mac[i:i+2] for i in range(0, len(decoded_mac), 2))

            print("MAC address of host {} is {}".format(ip, human_mac))
            host_list.append([ip, human_mac])
            print("List is", host_list)

    except KeyboardInterrupt:
        print("KeyboardInterrupt signal received, quitting", host_list)
        sys.exit(0)

    # print("ARP Sniffer Worker task complete")
    return host_list
