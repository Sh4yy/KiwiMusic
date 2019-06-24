from xmlr import xmliter
from pprint import pprint


class Artist:

	def __init__(self, json):
		self.id = json.get('id')
		self.name = json.get('name')
		self.profile = json.get('profile')
		self.realname = json.get('realname')
		self.data_quality = json.get('data_quality')

		self.aliases = None
		if "aliases" in json:
			self.aliases = json['aliases']['name']

		self.namevariations = None
		if 'namevariations' in json:
			self.namevariations = json['namevariations']['name']

		self.members = None
		if 'members' in json and json['members']:
			self.members = []
			for id, member in zip(json['members']['id'], json['members']['name']):
				self.members.append({'name': member, 'id': id})

		self.groups = None
		if 'groups' in json and json['groups']:
			self.groups = json['groups']['name']

		self.urls = None
		if 'urls' in json and json['urls']:
			self.urls = json['urls']['url']

	def __str__(self):
		return f"<Artist(id={self.id}, name={self.name})>"

	@classmethod
	def parse(cls, file_path):
		"""
		generator parser
		:param file_path: path to xml file
		:return: yields artist items
		"""

		for data in xmliter(file_path, 'artist'):
			yield cls(data)

class Master:

	def __init__(self, json):
		self.id = json.get('@id')
		self.year = json.get('year')
		self.data_quality = json.get('data_quality')
		self.main_release = json.get('main_release')
		self.title = json.get('title')
		self.notes = json.get('notes')

		self.artists = None
		if 'artists' in json and json['artists']:
			if type(json['artists']['artist']) == list:
				self.artists = json['artists']['artist']
			else:
				self.artists = [json['artists']['artist']]

		self.genres = None
		if 'genres' in json and json['genres']:
			if type(json['genres']['genre']) == list:
				self.genres = json['genres']['genre']
			else:
				self.genres = [json['genres']['genre']]

		self.styles = None
		if 'styles' in json and json['styles']:
			if type(json['styles']['style']) == list:
				self.styles = json['styles']['style']
			else:
				self.styles = [json['styles']['style']] 

		self.videos = None
		if 'videos' in json and json['videos']:
			if type(json['videos']['video']) == list:
				self.videos = json['videos']['video']
			else:
				self.videos = [json['videos']['video']]

	def __str__(self):
		return f"<Master(id={self.id}, title={self.title})>"

	@classmethod
	def parse(cls, file_path):
		"""
		generator parser
		:param file_path: path to xml file
		:return: yields Master items
		"""

		for data in xmliter(file_path, 'master'):
			yield cls(data)


class Release:

	def __init__(self, json):
		self.id = json.get('@id')
		self.country = json.get('country')
		self.data_quality = json.get('data_quality')
		self.title = json.get('title')
		self.notes = json.get('notes')
		self.master_id = json.get('master_id')
		self.status = json.get('@status')

		self.artists = None
		if 'artists' in json and json['artists']:
			if type(json['artists']['artist']) == list:
				self.artists = json['artists']['artist']
			else:
				self.artists = [json['artists']['artist']]

		self.genres = None
		if 'genres' in json and json['genres']:
			if type(json['genres']['genre']) == list:
				self.genres = json['genres']['genre']
			else:
				self.genres = [json['genres']['genre']]

		self.styles = None
		if 'styles' in json and json['styles']:
			if type(json['styles']['style']) == list:
				self.styles = json['styles']['style']
			else:
				self.styles = [json['styles']['style']]

		self.videos = None
		if 'videos' in json and json['videos']:
			if type(json['videos']['video']) == list:
				self.videos = json['videos']['video']
			else:
				self.videos = [json['videos']['video']]

		self.extraartists = None
		if 'extraartists' in json and json['extraartists']:
			if type(json['extraartists']['artist']) == list:
				self.extraartists = json['extraartists']['artist']
			else:
				self.extraartists = [(json['extraartists']['artist'])]

		self.formats = None
		if 'formats' in json and json['formats']:
			if type(json['formats']['format']) == list:
				self.formats = json['formats']['format']
			else:
				self.formats = [json['formats']['format']]

		self.tracklist = None
		if 'tracklist' in json and json['tracklist']:
			if type(json['tracklist']['track']) == list:
				self.tracklist = json['tracklist']['track']
			else:
				self.tracklist = [json['tracklist']['track']]

		self.companies = None
		if 'companies' in json and json['companies']:
			if type(json['companies']['company']) == list:
				self.companies = json['companies']['company']
			else:
				self.companies = [json['companies']['company']]

		self.identifiers = None
		if 'identifiers' in json and json['identifiers']:
			if type(json['identifiers']['identifier']) == list:
				self.identifiers = json['identifiers']['identifier']
			else:
				self.identifiers = [json['identifiers']['identifier']]

		self.labels = None
		if 'labels' in json and json['labels']:
			if type(json['labels']['label']) == list:
				self.labels = json['labels']['label']
			else:
				self.labels = [json['labels']['label']]

 
	def __str__(self):
		return f"<Release(id={self.id}, title={self.title})>"

	@classmethod
	def parse(cls, file_path):
		"""
		generator parser
		:param file_path: path to xml file
		:return: yields Release items
		"""

		for data in xmliter(file_path, 'release'):
			yield cls(data)

