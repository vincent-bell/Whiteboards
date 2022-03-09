	# absolute imports
import os
import subprocess
import openpyxl
import pandas as pd
from pathlib import Path
from typing import Tuple
try:
	from cryptography.fernet import Fernet
except ModuleNotFoundError:
	subprocess.call(['pip', 'install', 'cryptography'])
	from cryptography.fernet import Fernet

# relative imports
from ..utils.errors import SecurityError


DATA_KEY = 'SECRET_KEY'
ENCODING_FORMAT = 'utf-8'
WARNING = "[Security Warning] You must link the new key in others/whiteboards/security/unlock.key"


class Authenticator:
	"""
	class to handle the authentication and sign up of users for the whiteboards app.
	:param key: bytes
	:return: None
	"""
	def __init__(self, key: bytes = os.environ.get(DATA_KEY)):
		self.key_path = os.path.join(
			'whiteboards', 'security', 'unlock.key'
		)
		self.userdata_file = os.path.join(
			'whiteboards', 'userdata', 'enc_users.xlsx'
		)
		
		if key:
			self.__key = bytes(key, ENCODING_FORMAT)
		else:
			self.make_new_key()
			raise SecurityError(WARNING)


	def make_new_key(self) -> None:
		"""
		method generates a new key and writes it to the path in self.key_path
		:return: None
		"""
		key = Fernet.generate_key()
		with open(self.key_path, 'wb') as unlock:
			unlock.write(key)


	def encrypt_file(self, target: Path, outpath: Path = None) -> None:
		"""
		method encrypts a file specified in file_path with a key specified
		in key and writes the contents to either a specified outpath or the original file
		:param file_path: Path
		:param outpath: Path
		:return: None
		"""

		lock = Fernet(self.__key)
				
		with open(target, 'rb') as file:
			file_contents = file.read()
		encrypted_file_contents = lock.encrypt(file_contents)
		
		if outpath:
			with open(outpath, 'wb') as file:
				file.write(encrypted_file_contents)
		else:
			with open(target, 'wb') as file:
				file.write(encrypted_file_contents)


	def decrypt_file(self, target: Path) -> None:
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
		with open(target, 'wb') as file:
			file.write(decrypted_file_contents)


	def decrypt_dataframe(self) -> None:
		"""
		method sets up self.__dataframe
		:return: None
		"""
		self.decrypt_file(target=self.userdata_file)
		dataframe = pd.read_excel(self.userdata_file, engine='openpyxl')
		self.encrypt_file(target=self.userdata_file)
		self.__dataframe = dataframe
		self.drop_unnamed_columns()
		print(self.__dataframe)


	def drop_unnamed_columns(self) -> None:
		"""
		method 
		"""
		for col in self.__dataframe.columns:
			if 'Unnamed' in col:
				self.__dataframe = self.__dataframe.drop(labels=[col], axis=1)


	def authenticate(self, username: str, password: str) -> True or None:
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

	def sign_up(self, username: str, password: str, password_conf: str) -> Tuple[None, str] or Tuple[bool, None]:
		"""
		method attempts to sign up a user with the information supplied
		:param username: str
		:param password: str
		:param password_conf: str
		:return: Tuple(None, str) or Tuple(bool, None)
		"""
		NUMBERS = "0123456789"

		if len(username) < 6:
			return None, 'INV_USER_LEN'

		for character in username:
			if ord(character) in range(65, 91) or ord(character) in range(97, 123) or character in NUMBERS:
				pass
			else:
				return None, 'ALPHABET_E'

		data_len = len(self.__dataframe)
		for userid in range(data_len):
			existing_user = self.__dataframe.username[userid]
			if username == existing_user:
				return None, 'A_EXIST' 

		if len(password) < 8:
			return None, 'INV_PASS_LEN'

		if not password == password_conf:
			return None, 'PASS_NE'

		self.decrypt_file(target=self.userdata_file)
		new_frame = pd.DataFrame([[username, password]], columns=['username', 'password'], index=[len(self.__dataframe)])
		self.__dataframe = pd.concat([self.__dataframe, new_frame], verify_integrity=True)
		self.drop_unnamed_columns()
		self.__dataframe.to_excel(self.userdata_file, engine='openpyxl')
		self.encrypt_file(target=self.userdata_file)
		
		# TODO: Add the username and password to the current dataframe, encrypt it and rewrite the current file enc_users.xls
		# TODO: Research saving dataframes and adding entries before git flow finishing the feature

		return True, None
