import os
import sys
import re

# generate hotp
import hmac
import hashlib
import struct

from cryptography.fernet import Fernet # for encryption

def is_hexadecimal(arg):
	if len(arg) < 64:
		print (f"Error: The second argument should be at minimum field with 64 characters: {arg}")
		return False

	# check if the input is in the hexadecimal format	
	if re.match(r'^[0-9a-fA-F]+$', arg):
		return True
	else:
		print (f"Error: The second argument should be in hexadecimal format: {arg}")
		return False
 
def get_and_increment_counter():
	counter = 0
	try:
		with open('ft_otp_counter.txt', 'r') as file:
			counter = int(file.read().strip())
			if counter.isdigit():
				return int(counter)
			else:
				print ('File is corrupt: counter reset to zero')
	except Exception as e:
		pass
	
	counter += 1

	try:
		with open('ft_otp_counter.txt', 'w') as file:
			file.write(str(counter))
	except FileNotFoundError:
		print (f"Error: File not found: {key_file_path}")
		sys.exit(1)
	except ValueError:
		print (f"Error: The content of the file is corrupt: {key_file_path}")
		sys.exit(1)
	except PermissionError:
		print (f"Error: Permission refused: {key_file_path}")
		sys.exit(1)
	except Exception as e:
		print(f"An unexpected error append: {e}")
		sys.exit(1)
	
	return counter

def generate_hotp(key, counter):
	digits = 6
	secret_key = bytes.fromhex(key)  # Conversion in bytes
	# convert counter in octet because HMAC works in binary
	counter_bytes = struct.pack(">Q", counter)
    # Create an HMAC with the secret key and the counter
	hmac_result = hmac.new(secret_key, counter_bytes, hashlib.sha1).digest()
    # obtain the offset from the last 4 bits of the HMAC
	offset = hmac_result[-1] & 0xf
    # obtain an integer from the last 4 octets of HMAC by starting by the offset
	code = struct.unpack(">I", hmac_result[offset:offset+4])[0] & 0x7fffffff
    # Reduce the integer so it goes with the good amount of numbers
	code = code % (10 ** digits)
	return str(code).zfill(digits)

def decrypt_key(encrypted_key, encryption_key):
	decryptor = Fernet(encryption_key)
	try:
		return decryptor.decrypt(encrypted_key).decode()
	except Exception as e:
		print(f"Error during decryption: {e}")
		return None

def k_parsing(key_file_path, encryption_key):
	# read the encrypted hexa key
	try:
		with open(key_file_path, 'rb') as key_file:
			encrypted_key = key_file.read()
	except FileNotFoundError:
		print (f"Error: File not found: {key_file_path}")
		sys.exit(1)
	except ValueError:
		print (f"Error: The content of the file is corrupt: {key_file_path}")
		sys.exit(1)
	except PermissionError:
		print (f"Error: Permission refused: {key_file_path}")
		sys.exit(1)
	except Exception as e:
		print(f"An unexpected error append: {e}")
		sys.exit(1)

	# Decrypt the hexa key file 
	hex_key = decrypt_key(encrypted_key, encryption_key)
	if (is_hexadecimal(hex_key) == False):
		sys.exit(1)

	# generate the otp
	counter = get_and_increment_counter()
	otp = generate_hotp(hex_key, counter)
	print(f"The single use password is: {otp}")


def encrypt_and_save_key(hex_key):
	# Generate an encryption key
	encryption_key = Fernet.generate_key()
	secure_encryption = Fernet(encryption_key)

	# hexa encryption key
	encrypted_hexa = secure_encryption.encrypt(hex_key.encode())

	# stock hexa encrypted key in the file
	try:
		with open('ft_otp.key', 'wb') as file:
			file.write(encrypted_hexa)
	except Exception as e:
		print(f"An unexpected error append: {e}")
		sys.exit(1)

	return encryption_key # need to return the value

def save_encryption_key(encryption_key):
	encryption_key_filename = input("Enter a filename to save the encrypted key in a secure way: ")

	try:
		with open(encryption_key_filename, 'wb') as key_file: # create and write the key into the file
			key_file.write(encryption_key)
	except KeyboardInterrupt:
		print("\nOperation cancelled by user.")
		sys.exit(0)
	except Exception as e:
		print(f"An unexpected error append: {e}")
		sys.exit(1)
	
	print(f"The encrypted key has been saved in '{encryption_key_filename}'. Keep this file safe.")

def parse_input(*args):
	if len(args) > 2:
		print ("Error: More than two arguments in command line, please follow the format: ./ft_otp [-gk] [FILE]")
		return
	
	if len(args) < 2:
		print ("Error: Not enough arguments in the comand ligne, please follow the format: ./ft_otp [-gk] [FILE]")
		return

	first_arg = args[0]
	second_arg = args[1]

	if first_arg not in ["-k", "-g"]:
		print (f"Error: The option is not correct: {first_arg}, please follow the format: ./ft_otp [-gk] [FILE]")
		return

	if first_arg == "-g":
		if os.path.isfile(second_arg):
			try:
				with open(second_arg, 'r') as file:
					content = file.read().strip()
			except Exception as e:
				print(f"An unexpected error append: {e}")
				sys.exit(1)
		else:
			content = second_arg
		
		if is_hexadecimal(content):
			encryption_key = encrypt_and_save_key(content)
			save_encryption_key(encryption_key)
		else:
			return

	else:
		if second_arg != "ft_otp.key":
			print("Error : The file specified must be 'ft_otp.key'")
			sys.exit(1)
		encryption_key = input("Please enter the encryption key to decrypt the hexadecimal key: ")
		k_parsing(second_arg, encryption_key)

def main():
	try:
		arguments = sys.argv[1:]
		parse_input(*arguments)
	except KeyboardInterrupt:
		print("\n[Info] Script execution interrupted by user.")
		sys.exit(0)
	except Exception as e:
		print(f"\n[Error] An unexpected error occurred: {e}")
		sys.exit(1)

if __name__ == '__main__':
    main()