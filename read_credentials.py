import configparser
import os

def get_credentials(path):
        config = configparser.RawConfigParser()
        #path = os.path.join(os.path.expanduser('~'), path)
        print('credentials path is ',path)
        config.read(path)
        token_read = config.get('default', 'personal_access_token')
        return(token_read)
