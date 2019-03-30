import os, random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

def encrypt(key, filename):
	chunksize = 256*4096
	outputFile = "lencryptedl"+filename
	filesize = str(os.path.getsize(filename)).zfill(16)
	IV = ''

	for i in range(16):
		IV += chr(random.randint(0, 0xFF))

	encryptor = AES.net(key, AES.MODE_CBC, IV)

	with open(filename, 'rb') as infile:
		with open(outputFile, 'wb') as outfile:
			outfile.write(filesize)
			outfile.write(IV)

			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break
				elif len(chunk) % 16 != 0:
					chunk += ' ' * (16 - (len(chunk) % 16))

				outfile.write(encryptor.encrypt(chunk))

def decrypt(key, filename):
	chunksize = 256*4096
	outputFile = filename[11:]

	with open(filename, 'rb') as infile:
		filesize = long(infile.read(16))
		IV = infile.read(16)

		decryptor = AES.new(key, AES.MODE_CBC, IV)

		with open(outputFile, 'wb') as outfile:
			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break

				outfile.write(decryptor.decrypt(chunk))
			outfile.truncate(filesize)

def getKey(password):
	hasher = SHA256.new(password)
	return hasher.digest()

def Main():
	choice = raw_input('Encrypt Or Decrypt?:')

	if choice == 'E':
		filename = raw_input('Filename:')
		password = raw_input('Password:')
		encrypt(getKey(password), filename)
		print('Encrypted')
	elif choice == 'D':
		filename = raw_input('Filename:')
		password = raw_input('Password:')
		decrypt(getKey(password), filename)
		print('Decrypted')
	else:
		print'No Option Selected'

Main()
