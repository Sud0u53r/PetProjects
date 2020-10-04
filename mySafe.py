#!/usr/bin/python3
import argparse, sqlite3, getpass, os, random, sys, time, io, atexit, base64
from Crypto.Cipher import AES
from hashlib import md5
from tabulate import tabulate
import clipboard

parser = argparse.ArgumentParser(description = 'Testing')
parser.add_argument('-i', metavar = 'dbname', type = str, nargs = "*", help = 'Initializes by creating a new db')
parser.add_argument('-f', metavar = '<filename>', type = str, help = 'Name of locker to open')
parser.add_argument('-o', metavar = '<options>', type = int, help = 'Options for the mainmenu')
parser.add_argument('-c', metavar = '<ID>', type = int, help = 'ID of the record to copy it\'s password')
parser.add_argument('--show-all-passwords', help = 'Display all the records along with passwords', action='store_true')

schema = '''
CREATE TABLE IF NOT EXISTS safebox (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	title VARCHAR(120) NOT NULL,
	username VARCHAR(120) NOT NULL,
	password VARCHAR(120) NOT NULL,
	notes VARCHAR(300) NOT NULL,
	last_modified VARCHAR(120) NOT NULL
);
'''

def hash_from_pass(password):
	hash = password.encode()
	for _ in range(10): hash = md5(hash).hexdigest().encode()
	return hash.decode()

class AESCipher:
	def __init__(self, key):
		self.bs = 16
		self.key = key

	def encrypt(self, data):
		if type(data) == str: data = data.encode()
		data = self.pad(data)
		iv = bytes([random.randint(0, 0xff) for _ in range(self.bs)])
		enc = AES.new(self.key, AES.MODE_CBC, iv)
		return iv + enc.encrypt(data)

	def decrypt(self, enc_data):
		iv = enc_data[:self.bs]
		dec = AES.new(self.key, AES.MODE_CBC, iv)
		return self.unpad(dec.decrypt(enc_data[self.bs:]))

	def pad(self, data):
		return data + b''.join(b'\0' for _ in range(self.bs - (len(data) % self.bs)))

	def unpad(self, data):
		return data.rstrip(b'\0')

def query_db(dbfile, query, params = []):
	try:
		db_conn = sqlite3.connect(dbfile)
		cur = db_conn.cursor()
		cur.execute(query, params)
		res = cur.fetchall()
		db_conn.commit()
	except:
		exit('The locker and the password combo didn\'t work!')
	finally:
		db_conn.close()
	return res

def new_box(filename = 'locker'):
	if os.path.exists(filename):
		exit('A DB with that name (locker) already exists!')
	mainPass = getpass.getpass('Enter the master password for the new DB: ')
	pass_hash = hash_from_pass(mainPass)
	query_db(filename, schema)
	with open(filename, 'rb') as f: locker_data = f.read()
	aesObj = AESCipher(pass_hash)
	enc_locker_data = aesObj.encrypt(locker_data)
	with open(filename, 'wb') as f: f.write(enc_locker_data)

def show_records(filename, ID = ''):
	if ID:
		res = query_db(filename, "SELECT id, title, username, notes, last_modified FROM safebox WHERE id = ?;", ID)
	else:
		res = query_db(filename, "SELECT id, title, username, notes, last_modified FROM safebox;")
	if not res: return [], ""
	return res, tabulate(res, headers = ['ID', 'Title', 'Username', 'Notes', 'Last Modified'], tablefmt='pretty')

def show_all_record_titles(filename):
	res = query_db(filename, "SELECT id, title FROM safebox;")
	if not res: return [], ""
	return res, tabulate(res, headers = ['ID', 'Title'], tablefmt='pretty')

def get_a_record(filename, ID):
	res = query_db(filename, "SELECT * FROM safebox WHERE id = ?;", str(ID))
	if len(res) != 1:
		return []
	else:
		return res[0]

def show_complete_table(filename):
	res = query_db(filename, "SELECT * FROM safebox;")
	if not res: return [], ''
	return res, tabulate(res, headers = ['ID', 'Title', 'Username', 'Password', 'Notes', 'Last Modified'], tablefmt='pretty')

def mainMenu(filename, inp = None):
	if inp is None:
		print('1) Show all records\n2) Insert new record\n3) Edit existing record\n4) Delete existing record\n5) Delete all records')
		inp = int(input('Enter your choice: '))
	if inp not in [1, 2, 3, 4, 5]:
		exit('Select only available options')
	if inp == 1:
		res, all_records = show_records(filename)
		print(all_records) if res else exit('> No records to show!')
		print('To copy use this command with the respective ID.\n./main.py -f %s -c <ID>'%filename)
	elif inp == 2:
		title = input('Title: ')
		username = input('Username: ')
		password = getpass.getpass('Password: ')
		if not password: password = base64.b64encode(bytes([random.randint(0, 0xff) for _ in range(random.randrange(5,15))])).decode().strip('=')
		notes = input('Notes: ')
		if not notes: notes = '-'*10
		last_modified = time.strftime('%d/%m/%Y %I:%M:%S %p')
		query_db(filename, "INSERT INTO safebox(title, username, password, notes, last_modified) VALUES(?, ?, ?, ?, ?);", [title, username, password, notes, last_modified])
		print('> Record successfully inserted')
	elif inp == 3:
		res, record_titles = show_all_record_titles(filename)
		inp = input('Enter the record id to edit: ')
		if int(inp) not in [x[0] for x in res]:
			exit('Enter only id of existing record')
		res = get_a_record(filename, inp)
		username = input('Username: ')
		password = getpass.getpass('Password: ')
		if not password: password = base64.b64encode(bytes([random.randint(0, 0xff) for _ in range(random.randrange(5,15))])).decode().strip('=')
		notes = input('Notes: ')
		if not notes: notes = '-'*10
		last_modified = time.strftime('%d/%m/%Y %I:%M:%S %p')
		query_db(filename, "UPDATE safebox SET username = ?, password = ?, notes = ?, last_modified = ?", [username, password, notes, last_modified])
		print('> Record edited successfully')
	elif inp == 4:
		res, record_titles = show_all_record_titles(filename)
		print(record_titles) if res else exit('> No records to delete!')
		inp = input('Enter the record id to delete: ')
		if int(inp) not in [x[0] for x in res]:
			exit('Enter only id of existing record')
		safety = input('Do you really want to delete this? [Y/n]: ')
		if safety == 'Y': 
			query_db(filename, "DELETE FROM safebox WHERE id = ?", inp)
			exit('> Record successfully deleted')
	elif inp == 5:
		safety = input('Do you really want to delete all the records? [Y/n]: ')
		if safety == 'Y': 
			query_db(filename, "DELETE FROM safebox;")
			exit('> All the records has been successfully deleted')
		else:
			exit('> No record has been deleted')

if __name__ == '__main__':
	if len(sys.argv) < 2:
		exit('python3 %s -h for help'%sys.argv[0])
	args = parser.parse_args()
	if args.i is not None:
		ll = len(args.i)
		if ll == 0:
			new_box()
		elif ll == 1:
			new_box(args.i[0])
		else:
			print('Only one filename should be given!')
		exit()
	if args.f is not None:
		org_filename = args.f
		if not os.path.exists(org_filename): exit('Locker with that name doesn\'t exist!')
		mainPass = getpass.getpass('Enter master password for the locker: ')
		pass_hash = hash_from_pass(mainPass)
		aesObj = AESCipher(pass_hash)
		with open(org_filename, 'rb') as f: enc_locker_data = f.read()
		locker_data = aesObj.decrypt(enc_locker_data)
		filename = '.' + org_filename
		with open(filename, 'wb') as f: f.write(locker_data)
		atexit.register(os.remove, filename)
		query_db(filename, 'SELECT 123 FROM safebox;') # For testing the password
		if args.c is not None:
			copy_id = args.c
			record = get_a_record(filename, copy_id)
			if not record: exit('There is not record with given ID!')
			clipboard.copy(record[3])
			print('Password is copied to clipboard and will be erased in 5 seconds')
			for i in [5, 4, 3, 2, 1, 'X X X']:
				print('\r%s'%i, end = '')
				time.sleep(1)
			clipboard.copy('Not Your Password!')
			print('\r\nPassword erased!')
			exit()
		elif args.show_all_passwords is not None:
			prompt = input('Do you really want to see all the passwords? [YES/n]: ')
			if prompt == 'YES':
				res, table = show_complete_table(filename)
				exit(table)
			else:
				exit('Exit!')
		else:
			mainMenu(filename, args.o)
		with open(filename, 'rb') as f: locker_data = f.read()
		enc_locker_data = aesObj.encrypt(locker_data)
		with open(org_filename, 'wb') as f: f.write(enc_locker_data)
