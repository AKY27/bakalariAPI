from bakaAPI import API, LoginError
import os, requests, json, time
from dotenv import load_dotenv, set_key

load_dotenv()

SCHOOL_URL = os.getenv("SCHOOL_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

baka = API(SCHOOL_URL=SCHOOL_URL, USERNAME=USERNAME, PASSWORD=PASSWORD, REFRESH_TOKEN=REFRESH_TOKEN)

try:
    baka.refresh()
except LoginError:
    baka.login()
    set_key(".env", "REFRESH_TOKEN", baka.REFRESH_TOKEN)







'''
done = False
while not(done):
    if (time.time() > baka.expiration-(baka.expiration-time.time())/2):
        baka.refresh()
        print("connection refreshed")
    
    time.sleep(600)
    print("sleeping  " + str(time.time()))
    '''