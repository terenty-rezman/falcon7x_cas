import requests
from time import sleep

requests.get("http://127.0.0.1:8881/api/show_message", json = {"message": "BLEED: APU FAULT"})

sleep(5)

requests.get("http://127.0.0.1:8881/api/remove_message", json = {"message": "BLEED: APU FAULT"})