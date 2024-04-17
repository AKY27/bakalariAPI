from flask import Flask, render_template, send_file, jsonify
from bakaAPI import API, LoginError
import os, json, time
from dotenv import load_dotenv, set_key

load_dotenv()

SCHOOL_URL = os.getenv("SCHOOL_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
OFFSET = os.getenv("OFFSET")

baka = API(SCHOOL_URL=SCHOOL_URL, USERNAME=USERNAME, PASSWORD=PASSWORD, REFRESH_TOKEN=REFRESH_TOKEN)

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("./index.html")

@app.route('/api/actual/<date>')
def actual(date):
    try:
        baka.refresh()
    except LoginError:
        baka.login()
        set_key(".env", "REFRESH_TOKEN", baka.REFRESH_TOKEN)
    if date == "today":
        today = list(time.localtime(time.time() + int(OFFSET))) # + OFFSET to show the schedule earlier or later, can be not used
        date = f"{today[0]:04}-{today[1]:02}-{(today[2]):02}"
    data = baka.get_actual(date=date)
    with open("./static/data/timetable.json", "w") as f:
        f.write(json.dumps(data, sort_keys=False, indent=2))
    return send_file("./static/data/timetable.json")

@app.route('/api/permanent')
def permanent():
    try:
        baka.refresh()
    except LoginError:
        baka.login()
        set_key(".env", "REFRESH_TOKEN", baka.REFRESH_TOKEN)
    data = baka.get_permanent()
    with open("./static/data/permanent.json", "w") as f:
        f.write(json.dumps(data, sort_keys=False, indent=2))
    return send_file("./static/data/permanent.json")

@app.route("/main.js")
def main_js():
    return send_file("./static/js/main.js")

@app.route("/bg_img.png")
def bg_img():
    return send_file("./static/img/bg_img.png")

if __name__ == '__main__':
    app.run(debug=True, port=8000)