	# absolute imports
import os
import subprocess as subproc
import xlrd
import pandas as pd
from pathlib import Path
try:
	from cryptography.fernet import Fernet
except ModuleNotFoundError:
	subproc.call(['pip', 'install', 'cryptography'])
	from cryptography.fernet import Fernet

# relative imports
from ..utils.errors import SecurityError


DATA_KEY = 'SECRET KEY'
ENCODING_FORMAT = 'utf-8'
WARNING = "[Security Warning] You must link the new key in others/whiteboards/security/unlock.key"


class Authenticator:
	"""
	Class to handle the authentication of users for whiteboards app.
	Handling of userdata is designed to be secure and symmetric 
	encryption is used in order to cope with this.
	:param key: bytes
	:return: None
	"""
	def __init__(self, key: bytes = os.environ.get(DATA_KEY)):
		self.key_path = os.path.join(
			'others', 'whiteboards', 'security', 'unlock.key'
		)
		self.userdata_path = os.path.join(
			'others', 'whiteboards', 'userdata', 'enc_users.xls'
		)
		
		if key:
			self.__key = bytes(key, ENCODING_FORMAT)
		else:
			self.make_new_key()
			raise SecurityError(WARNING)


	def make_new_key(self):
		"""
		method generates a new key and writes it to the path in self.key_path
		:return: None
		"""
		key = Fernet.generate_key()
		with open(self.key_path, 'wb') as unlock:
			unlock.write(key)


	def encrypt_file(self, target: Path, outpath: Path = None):
		"""
		method encrypts a file specified in file_path with a key specified
		in key and writes the contents to outpath
		:param file_path: Path
		:param outpath: Path
		:return: None
		"""
		# if an outpath is not specified then set it to original location with name enc_{filename}.ext
		if not outpath:
			outpath = ""
			outpath_file = 'enc_{f}'.format(f=file_path.split('/')[-1])
			path_parts = file_path.split('/')[0:-1]
			for part in path_parts:
				outpath = os.path.join(outpath + part + '/')
			outpath.join(path_parts)
			outpath = outpath + outpath_file
			print(f'{outpath=}, {type(outpath)}')

		lock = Fernet(self.__key)
				
		with open(target, 'rb') as file:
			file_contents = file.read()
		encrypted_file_contents = lock.encrypt(file_contents)
			
		with open(outpath, 'wb') as outfile:
			outfile.write(encrypted_file_contents)


	def decrypt_file(self, target: Path) -> bytes:
		"""
		method decrypts the file in file_path with the key specified in key
		set self.key once an unlock.key file is set? 
		:param file_path: Path
		:return file_contents: bytes
		"""
		unlock = Fernet(self.__key)
		with open(target, 'rb') as file:
			file_contents = file.read()
		decrypted_file_contents = unlock.decrypt(file_contents)
		return decrypted_file_contents


	def decrypt_dataframe(self):
		"""
		method decrypts the userdata and creates a pandas dataframe
		then stores the dataframe in a private attr: self.__dataframe
		:return: None
		"""
		userdata = self.decrypt_file(target=self.userdata_path)
		dataframe = pd.read_excel(userdata, engine='xlrd')
		self.__dataframe = dataframe


	def authenticate(self, username: str, password: str):
		"""
		method attempts to authenticate a user based on the values of username and password
		:param username: str
		:param password: str
		:return: True or None
		"""
		data_len = len(self.__dataframe)
		for userid in range(data_len):
			working_user = self.__dataframe.username[userid]
			working_pass = self.__dataframe.password[userid]
			if username == working_user and password == working_pass:
				return True
		return None
