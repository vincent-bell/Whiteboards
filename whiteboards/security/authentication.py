# absolute imports
import os
import subprocess
import pandas as pd
from pathlib import Path
from typing import Tuple
from cryptography.fernet import Fernet

# relative imports
from ..utils.errors import SecurityError


ENCRYPTION_KEY = "2t2eEDW62bP7mAt80GxekbjJacR44XBJHSeZBXA2E6o="
ENCODING_FORMAT = "utf-8"


class Authenticator:
	def __init__(self, key: bytes = ENCRYPTION_KEY):
		self.__key = bytes(key, ENCODING_FORMAT)
		self.userdata_file = os.path.join(
			'whiteboards', 'userdata', 'enc_users.xlsx'
		)


	def encrypt_file(self, target: Path, outpath: Path = None) -> None:
		"""
		This method encrypts a file specified by target with the key specified in $env:SECRET_KEY
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
		This method decrypts the file specified by target with the key specified in $env:SECRET_KEY.
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
		This method decrypts the userdata and stores the registered users
		in a private attribute self.__dataframe.
		:return: None
		"""
		self.decrypt_file(target=self.userdata_file)
		dataframe = pd.read_excel(self.userdata_file, engine='openpyxl')
		self.encrypt_file(target=self.userdata_file)
		self.__dataframe = dataframe
		self.drop_unnamed_columns()


	def drop_unnamed_columns(self) -> None:
		"""
		This method drops unnamed columns from self.__dataframe which are generated
		as excess columns when a new user is registered.

		"""
		for col in self.__dataframe.columns:
			if 'Unnamed' in col:
				self.__dataframe = self.__dataframe.drop(labels=[col], axis=1)


	def authenticate(self, username: str, password: str) -> True or None:
		"""
		This method attempts to authenticate a user based on the values of username and password.
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
		This method attempts to sign up a user with the information supplied.
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

		for userid in range(len(self.__dataframe)):
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
		
		return True, None
