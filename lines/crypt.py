# from Crypto.Cipher import DES

# KEY = "key_test" # key must be made by 8 chars (8 bytes)

# def encrypt(text, key=KEY):
# 	# ATTENZIONE: non cryptare testi con spazi finali o iniziali
# 	des = DES.new(key, DES.MODE_ECB)

# 	if len(text)%8:
# 		text += " "*(8-len(text)%8)
# 	return des.encrypt(text)

# def decrypt(text_encrypted, key=KEY):
# 	des = DES.new(key, DES.MODE_ECB)
# 	return des.decrypt(text_encrypted)

from Crypto.Cipher import AES

def encrypt(text):
 	if len(text)%8:
 		text += " "*(16-len(text)%16)
	encryption_suite = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
	cipher_text = encryption_suite.encrypt(text)
	return cipher_text

def decrypt(text_encrypted):
	decryption_suite = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
	plain_text = decryption_suite.decrypt(text_encrypted)
	return plain_text


if __name__ == '__main__':
	text = "ciao come va"
	encrypted_text = encrypt(text)
	print(encrypted_text)

	decrypted_text = decrypt(encrypted_text)
	print(decrypted_text)

	import random

	text = repr(random.getstate())
	with open("/tmp/x.txt", "w") as f:
		encrypted_text = encrypt(text)
		f.write(encrypted_text)

	print(random.randint(0,9))

	with open("/tmp/x.txt") as f:
		encrypted_text = f.read()
		text = decrypt(encrypted_text)
		random.setstate(eval(text))

	print(random.randint(0,9))