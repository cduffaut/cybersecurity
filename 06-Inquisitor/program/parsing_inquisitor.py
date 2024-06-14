import sys # se servir de l'input 
import ipaddress # valider l'adresse ip
import re # valider l'adresse mac

"""
	--- Partie parsing ---
"""

# : str pour informer que l'arg est un str
# -> bool pour dire qu'il retourne un booleen
def parse_mac(mac_address: str) -> bool:
	# fait correspondre mac_address avec une expression régulière 
	# qui définit le format attendu d'une adresse MAC.
	is_valid_mac = re.match(r'([0-9A-F]{2}[:]){5}[0-9A-F]{2}|' # format ':' s
                        r'([0-9A-F]{2}[-]){5}[0-9A-F]{2}', # format des '-'
                        string=mac_address,
                        flags=re.IGNORECASE) # traiter txt MAJ et min de maniere equivalente
	try:
		return bool(is_valid_mac.group())
	except AttributeError:
		return False

def parse_ip(ip1, ip2):
	try:
		addr1 = ipaddress.ip_address(ip1)
		addr2 = ipaddress.ip_address(ip2)

		if (addr1.version != 4 or addr2.version != 4):
			print ('Error\n\033[0;31mAt least one of the two IP\'s are not in the right format.')
			exit (1)
	except ValueError:
		print ('Error\n\033[0;31mAt least one of the two IP\'s are not in the right format.')
		exit(1)

def parsing_inputs():
	if len(sys.argv) != 5:
		print ('Error\n\033[0;31mPlease respect the format for the inquisitor program: \033[0mpython3 inquisitor.py <IP-src> <MAC-src> <IP-target> <MAC-target>')
		exit (1)
	
	elif sys.argv[1] == sys.argv[3]:
		print ('Error\n\033[0;31mIPV4 addresses are the same.\033[0m')
		exit (1)
	
	elif sys.argv[2] == sys.argv[4]:
		print ('Error\n\033[0;31mMAC addresses are the same.\033[0m')
		exit (1)

	parse_ip(sys.argv[1], sys.argv[3])
	if not parse_mac (sys.argv[2]) or not parse_mac(sys.argv[4]):
		print ('Error\n\033[0;31mAt least one of the two MAC addresses are not valid.')
		exit (1)	
