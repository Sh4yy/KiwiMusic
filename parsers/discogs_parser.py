from xmlr import xmliter
from pprint import pprint
from abc import ABC, abstractmethod
import json as JSON
import hashlib


class Parser(ABC):

    def __init__(self, json):
        """
        default initializer
        :param json: json data
        """
        self.json = json

    def hash(self, hash_method=hashlib.md5):
        """
        create a hash of the provided data
        :param hash_method: hashlib hash function
        :return: hex digest of the hash
        """
        return (hash_method(JSON.dumps(self.json, sort_keys=True))
                .hexdigest())

    @staticmethod
    def helper_remove_at_sign(json):
        """
        remove @ from keys in json
        :param json: json data
        :return: dict
        """
        resp = {}
        for key, value in json.items():
            if key.startswith('@'):
                key = key[1:]
            resp[key] = value
        return resp

    @staticmethod
    def helper_make_list(json, path):

        dirs = path.split('/')
        data = json
        for cur_dir in dirs:
            if not data: return None
            if cur_dir in data:
                data = data[cur_dir]
            else:
                return None

        return data if type(data) == list else [data]

    @classmethod
    @abstractmethod
    def parse(cls, file_path):
        pass


class Artist(Parser):

    def __init__(self, json):
        Parser.__init__(self, json)
        self.id = json.get('id')
        self.name = json.get('name')
        self.profile = json.get('profile')
        self.realname = json.get('realname')
        self.data_quality = json.get('data_quality')

        self.aliases = self.helper_make_list(json, "aliases/name")
        self.namevariations = self.helper_make_list(json, "namevariations/name")
        self.members = self.helper_make_list(json, 'members/name')
        self.groups = self.helper_make_list(json, "groups/name")
        self.urls = self.helper_make_list(json, "urls/url")

        while self.urls and None in self.urls:
            self.urls.remove(None)

        if 'members' in json and json['members']:
            self.members = []
            for id, member in zip(json['members']['id'], json['members']['name']):
                self.members.append({'name': member, 'id': id})

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


class Master(Parser):

    def __init__(self, json):
        Parser.__init__(self, json)
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
            self.videos = list(map(self.helper_remove_at_sign, self.videos))

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


class Release(Parser):

    def __init__(self, json):
        Parser.__init__(self, json)
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
            self.videos = list(map(self.helper_remove_at_sign, self.videos))

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
            self.formats = list(map(self.helper_remove_at_sign, self.formats))

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
            self.identifiers = list(map(self.helper_remove_at_sign, self.identifiers))

        self.labels = None
        if 'labels' in json and json['labels']:
            if type(json['labels']['label']) == list:
                self.labels = json['labels']['label']
            else:
                self.labels = [json['labels']['label']]
            self.labels = list(map(self.helper_remove_at_sign, self.labels))

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
