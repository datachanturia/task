from flask import Flask
from flask import request
import requests
from bs4 import BeautifulSoup


def authorize(login, password):
    headers = {
        "X-OCTOBER-REQUEST-HANDLER": "onSignin",
        "X-Requested-With": "XMLHttpRequest"}
    payload = { "login": (None, login), "password": (None, password)}
    response = requests.post("http://applecity.ge/login", headers=headers, data=payload)

    if response.status_code != 200: 
        return False, None
    return True, response.cookies


def get_name_surname(cookies):
    response = requests.get("http://applecity.ge/profile", cookies=cookies)

    return parse_and_get_name(content=response.text)


def parse_and_get_name(content):
    soup = BeautifulSoup(content, "html.parser")
    return soup.find("input", {"id": "accountName"}).get("value")


app = Flask(__name__)


@app.route('/')
def apple_city_login():
    email = request.args.get("email")
    password = request.args.get("password")

    can_authorize, cookies = authorize(login=email, password=password)
    if can_authorize:
        return { 
            "status": 200, 
            "message": get_name_surname(cookies=cookies) }, 200
    return { 
        "status": 401, 
        "message": "bad credentials" }, 401

app.run(host='127.0.0.1', port=8000)