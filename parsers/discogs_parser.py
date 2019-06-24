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
        bin_data = JSON.dumps(self.json, sort_keys=True).encode()
        return hash_method(bin_data).hexdigest()

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

        self.artists = self.helper_make_list(json, "artists/artist")
        self.genres = self.helper_make_list(json, "genres/genre")
        self.styles = self.helper_make_list(json, "styles/style")

        self.videos = self.helper_make_list(json, "videos/video")
        self.videos = list(map(self.helper_remove_at_sign, self.videos or []))

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

        self.tracklist = self.helper_make_list(json, "tracklist/track")
        self.companies = self.helper_make_list(json, "companies/company")
        self.artists = self.helper_make_list(json, "artists/artist")
        self.genres = self.helper_make_list(json, "genres/genre")
        self.styles = self.helper_make_list(json, "styles/style")
        self.extraartists = self.helper_make_list(json, "extraartists/artist")

        self.videos = self.helper_make_list(json, "videos/video")
        self.videos = list(map(self.helper_remove_at_sign, self.videos or []))

        self.formats = self.helper_make_list(json, "formats/format")
        self.formats = list(map(self.helper_remove_at_sign, self.formats or []))

        self.identifiers = self.helper_make_list(json, "identifiers/identifier")
        self.identifiers = list(map(self.helper_remove_at_sign, self.identifiers or []))

        self.labels = self.helper_make_list(json, "labels/label")
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
