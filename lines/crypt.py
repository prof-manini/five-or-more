from Crypto.Cipher import DES

KEY = "key_test"
des = DES.new(KEY, DES.MODE_ECB)

def encrypt(text, key=KEY):
	# ATTENZIONE: non cryptare testi con spazi finali o iniziali
	des = DES.new(key, DES.MODE_ECB)

	if len(text)%8:
		text += " "*(8-len(text)%8)
	return des.encrypt(text)

def decrypt(text_encrypted, key=KEY):
	des = DES.new(key, DES.MODE_ECB)
	return des.decrypt(text_encrypted).strip()


if __name__ == '__main__':
	text = "ciao mondo."
	encrypted_text = encrypt(text)
	print(encrypted_text)

	decrypted_text = decrypt(encrypted_text)
	print(decrypted_text)