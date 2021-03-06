import os
import pandas as pd
from whiteboards.security.authentication import Authenticator
from whiteboards.utils.errors import SetupError


WARNING = "[Setup Fatal Error] Could not find users.xlsx or enc_users.xlsx"


def setup():
    """
    Function attempts to build enc_users.xlsx from users.xlsx if it does not exist.
    :return: None
    """
    target_path = os.path.join('whiteboards', 'userdata', 'users.xlsx')
    essential_path = os.path.join('whiteboards', 'userdata', 'enc_users.xlsx')
    if os.path.exists(target_path) and not os.path.exists(essential_path):
        authenticator = Authenticator()
        new_dataframe = pd.DataFrame([['default', 'password']], columns=['username', 'password'], index=[0])
        new_dataframe.to_excel(
            target_path,
            engine='openpyxl'
        )
        authenticator.encrypt_file(target=target_path, outpath=essential_path)
    else:
        if not os.path.exists(target_path) and not os.path.exists(essential_path):
            raise SetupError(WARNING)
