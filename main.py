"""This module provides script for discord account generation"""

import os
import string
from decouple import config
from twocaptcha import TwoCaptcha
import requests
import random
import json


API_URL = "https://discord.com/api/v9/auth/register"
solver = TwoCaptcha(config("API_KEY"))


def generate_password(length):
    """Generate password with specific length."""
    print("Generating password...")
    length = length
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    random.seed = (os.urandom(1024))

    return ''.join(random.choice(chars) for i in range(length))


def login(email, username):
    """Generate account using email and username"""

    print("Creating account...")
    s = requests.Session()
    captcha = solver.hcaptcha(
        sitekey="4c672d35-0701-42b2-88c3-78380b0db560",
        url="https://discord.com/register"
    )
    password = generate_password(16)
    s.headers["X-Fingerprint"] = s.get("https://discord.com/api/v9/experiments").json()["fingerprint"]
    fingerprint = s.headers["X-Fingerprint"]
    s.xsup = 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzkzLjAuNDU3Ny42MyBTYWZhcmkvNTM3LjM2IEVkZy85My4wLjk2MS40NyIsImJyb3dzZXJfdmVyc2lvbiI6IjkzLjAuNDU3Ny42MyIsIm9zX3ZlcnNpb24iOiIxMCIsInJlZmVycmVyIjoiaHR0cHM6Ly9kaXNjb3JkLmNvbS9jaGFubmVscy81NTQxMjU3Nzc4MTg2MTU4NDQvODcwODgxOTEyMzQyODUxNTk1IiwicmVmZXJyaW5nX2RvbWFpbiI6ImRpc2NvcmQuY29tIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjk3NTA3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=='
    s.headers = {
        'Host': 'discord.com', 'Connection': 'keep-alive',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'X-Super-Properties': s.xsup,
        'Accept-Language': 'en-US', 'sec-ch-ua-mobile': '?0',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47",
        'Content-Type': 'application/json', 'Authorization': 'undefined',
        'Accept': '*/*', 'Origin': 'https://discord.com',
        'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty', 'Referer': 'https://discord.com/register',
        'X-Debug-Options': 'bugReporterEnabled',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': 'OptanonConsent=version=6.17.0; locale=th'
    }
    try:
        register_patload = {
            "captcha_key": captcha["code"],
            "consent": True,
            "date_of_birth": "2004-05-06",
            "email": email,
            "fingerprint": fingerprint,
            "gift_code_sku_id": None,
            "invite": None,
            "password": password,
            "promotional_email_opt_in": False,
            "username": username,
        }

        res = s.post(url=API_URL, json=register_patload)
        if res.status_code == 201:
            print("Your token: " + json.loads(res.content)["token"])
        elif res.status_code == 429:
            print("You have sent to mach requests, please wait and try again")
        else:
            print("something went wrong, we got status code: " + str(res.status_code))
    except Exception as ex:
        print(str(ex))


if __name__ == "__main__":
    mail = input("Enter your email ")
    u_name = input("Enter your username ")
    login(mail, u_name)
