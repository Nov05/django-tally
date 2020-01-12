import os
import warnings

def checkEnviromentVariables():
    if 'RDS_DB_NAME' not in os.environ: 
        message = '''
You haven't set up environment variables for database.
Please Quit the server with CTRL-BREAK.
Set up RDS_DB_NAME, RDS_USERNAME, RDS_PASSWORD, RDS_HOSTNAME, RDS_PORT.
Then restart the server.'''
        warnings.warn(message, UserWarning)