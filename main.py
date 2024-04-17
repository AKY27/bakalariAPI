from bakaAPI import API
import os
from requests import HTTPError
from dotenv import load_dotenv, set_key

load_dotenv()

SCHOOL_URL = os.getenv("SCHOOL_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN") # if refresh token not in the .env file the strink will remain empty

baka = API(SCHOOL_URL=SCHOOL_URL, USERNAME=USERNAME, PASSWORD=PASSWORD, REFRESH_TOKEN=REFRESH_TOKEN) # create the API object

try:
    baka.refresh() # try to log in using refresh token
except HTTPError:
    baka.login() # login by credentials if the refresh token is not valid or missing
    set_key(".env", "REFRESH_TOKEN", baka.REFRESH_TOKEN) # save new refresh token to the .env file

'''
your own code here
'''