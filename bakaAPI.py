import os, requests, json, datetime

class API:
    def __init__(self, SCHOOL_URL, USERNAME, PASSWORD, REFRESH_TOKEN):
        self.SCHOOL_URL = SCHOOL_URL
        self.USERNAME = USERNAME
        self.PASSWORD = PASSWORD
        self.REFRESH_TOKEN = REFRESH_TOKEN
        self.headers={'Content-Type': 'application/x-www-form-urlencoded'}
    
    def login(self, ttl=4):
        data = {"Content-Type":"application/x-www-form-urlencoded","client_id":"ANDR","grant_type":"password","username":self.USERNAME,"password":self.PASSWORD}
        response = requests.post(os.path.join(self.SCHOOL_URL, "api/login"), data=data)
        if not(response.ok) and ttl:
            self.login(ttl=ttl-1)
        elif not(ttl):
            print("login failed")
            raise LoginError(response)
        else:       
            response_json = json.loads(response.content.decode("UTF-8"))
            self.ACCESS_TOKEN = response_json["access_token"]
            self.REFRESH_TOKEN = response_json["refresh_token"]
            
    def refresh(self, ttl=4):
        data = {"Content-Type":"application/x-www-form-urlencoded","client_id":"ANDR","grant_type":"refresh_token","refresh_token":self.REFRESH_TOKEN}
        response = requests.post(os.path.join(self.SCHOOL_URL, "api/login"), data=data)
        if not(response.ok) and ttl:
            self.refresh(ttl=ttl-1)
        elif not(ttl):
            print("refresh failed")
            raise LoginError(response)
        else:       
            response_json = json.loads(response.content.decode("UTF-8"))
            self.ACCESS_TOKEN = response_json["access_token"]
            self.REFRESH_TOKEN = response_json["refresh_token"]

    def get_actual(self, date="0000-00-00"):
        if date == "0000-00-00":
            date = str(datetime.date.today())
        headers = {"Content-Type":"application/x-www-form-urlencoded", "Authorization": f"Bearer {self.ACCESS_TOKEN}"}
        response = requests.get(os.path.join(self.SCHOOL_URL, f"api/3/timetable/actual?date={date}"), headers=headers)
        response_json = json.loads(response.content.decode("UTF-8"))
        return response_json
    
    def get_permanent(self):
        headers = {"Content-Type":"application/x-www-form-urlencoded", "Authorization": f"Bearer {self.ACCESS_TOKEN}"}
        response = requests.get(os.path.join(self.SCHOOL_URL, "api/3/timetable/permanent"), headers=headers)
        response_json = json.loads(response.content.decode("UTF-8"))
        return response_json
    
    def generate_logintoken(self):
        headers = {"Content-Type":"application/x-www-form-urlencoded", "Authorization": f"Bearer {self.ACCESS_TOKEN}"}
        response = requests.get(os.path.join(self.SCHOOL_URL, "api/3/logintoken"), headers=headers)
        response.raise_for_status()
        response_json = json.loads(response.content.decode("UTF-8"))
        return response_json
    
    def get_marks(self):
        headers = {"Content-Type":"application/x-www-form-urlencoded", "Authorization": f"Bearer {self.ACCESS_TOKEN}"}
        response = requests.get(os.path.join(self.SCHOOL_URL, "api/3/marks"), headers=headers)
        response_json = json.loads(response.content.decode("UTF-8"))
        return response_json
    



    

        


class LoginError(Exception):
    """
    could not login after 4 tries

    attributes:
        response
    """
    def __init__(self, response):
        self.message = json.loads(response.content.decode("UTF-8"))["error_description"]
        super().__init__(self.message)

class FetchError(Exception):
    """
    could not sucessfully fetch data from the server

    attributes:
        response
    """
    def __init__(self, response):
        self.message = json.loads(response.content.decode("UTF-8"))["error_description"]
        super.__init__(self.message)
