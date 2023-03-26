from nuvola_api import *
from notion_client import Client
from datetime import datetime
from yaml import safe_load

with open("config.yml", "r") as file:
	config = safe_load(file)

notion = Client(auth=config["credentials"]["notion_key"])
n = nuvola(config["credentials"]["username"], config["credentials"]["password"], config["credentials"]["student_id"])
try:
	n.login()
except WrongCredentialsException:
	print("wrong credentials!")
	quit()

def update(data):
	for i in data:
		print(i[1])
		new_page = {
		    "Name": {"title": [{"text": {"content": i[2]}}]},
		    "Date":{"date":{"start":i[1]}},
		    "Materia":{"select":{"name":i[0]}},
		    "Stato":{"select":{"name":"da fare"}}
		}
		notion.pages.create(parent={"database_id": config["credentials"]["database_id"]}, properties=new_page)


#update(n.compiti(12))
print(n.compiti(1))
