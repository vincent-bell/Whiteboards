import os
import subprocess
import pandas as pd
from whiteboards.security.authentication import Authenticator


if __name__ == '__main__':
    target_path = os.path.join('whiteboards', 'userdata', 'users.xlsx')
    authenticator = Authenticator()
    new_dataframe = pd.DataFrame([['default', 'password']], columns=['username', 'password'], index=[0])
    new_dataframe.to_excel(
        os.path.join('whiteboards', 'userdata', 'users.xlsx'),
        engine='openpyxl'
    )
    authenticator.encrypt_file(target='whiteboards/userdata/users.xlsx', outpath='whiteboards/userdata/enc_users.xlsx')