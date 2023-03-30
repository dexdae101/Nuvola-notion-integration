from nuvola_api import *
from notion_client import Client
from datetime import datetime
from yaml import safe_load


with open("config.yml", "r") as file:
	config = safe_load(file)

notion = Client(auth=config["credentials"]["notion_key"])
n = nuvola(config["credentials"]["username"], config["credentials"]["password"], config["credentials"]["student_id"])

used = {}

try:
	n.login()
except WrongCredentialsException:
	print("wrong credentials!")
	quit()

def update(data):
	for i in data:
		_hash = hash(str(i))
		if not _hash in used.keys():
			used[_hash] = datetime.now()
			print(i[1])
			'''new_page = {
			    "Name": {"title": [{"text": {"content": i[2]}}]},
			    "Date":{"date":{"start":i[1]}},
			    "Materia":{"select":{"name":i[0]}},
			    "Stato":{"select":{"name":"da fare"}}
			}
			notion.pages.create(parent={"database_id": config["credentials"]["database_id"]}, properties=new_page)'''
def cleanup(force=False):
	delete = []
	for i in used:
		delta = datetime.now() - used[i] 
		if delta.days > config["options"]["max_age"] or force:
			delete.append(i)
	for i in delete:
		del used[i]

update(n.compiti(12))
cleanup()
