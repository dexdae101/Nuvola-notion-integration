from json import loads
import requests
from bs4 import BeautifulSoup
import datetime

class nuvola():

	def __init__(self, username, password, student_id):
		self.username = username
		self.password = password
		self.student_id = student_id
		self.s = requests.Session()

	def newSession(self):
		self.s = requests.Session()

	def login(self):
		page = self.s.get("https://nuvola.madisoft.it/login")
		soup = BeautifulSoup(page.content, 'html.parser')
		csrf_token = soup.find_all('input')[0]['value']

		response = self.s.post('https://nuvola.madisoft.it/login_check', data={"_csrf_token":csrf_token, "_username":self.username, "_password":self.password})
		response = self.s.get("https://nuvola.madisoft.it/api-studente/v1/login-from-web")
		try:
			token = loads(response.content)['token']
			self.headers = {'Authorization':f'bearer {token}'}
		except Exception:
			raise WrongCredentialsException
		

	def compiti(self, days):
		try:
			d = datetime.datetime.now()
			start_date, start_time = d.date(), d.time()
			end_date, end_time = d.date(), d.time()
			end_date += datetime.timedelta(days=days)

			start_date = datetime.datetime.strftime(start_date, '%d-%m-%Y')
			end_date = datetime.datetime.strftime(end_date, '%d-%m-%Y')

			print(start_date, end_date)

			response = self.s.get(f"https://nuvola.madisoft.it/api-studente/v1/alunno/{self.student_id}/compito/elenco/{str(start_date)}/{str(end_date)}", headers=self.headers)
			response.raise_for_status()
			data = loads(str(response.content, "UTF-8"))
			out = []
			for i in data['valori']:
				out.append([i["materia"], i["dataConsegna"], i["descrizioneCompito"][0]])
			return out
		except requests.exceptions.RequestException as e:
			if response.status_code == 401:
				self.login()
				self.compiti()
			else:
				print(e)


class WrongCredentialsException(Exception):
    pass