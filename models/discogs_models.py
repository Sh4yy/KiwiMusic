from mongoengine import *


class Member(EmbeddedDocument):

    id = IntField()
    name = StringField()

    @classmethod
    def init(cls, member):
        """
        initialize Member model from Member dict
        :param member: member dict
        :return: member model
        """
        return cls(id=int(member['id']),
                   name=member['name'])


class ArtistDB(Document):

    meta = {
        'collection': 'artists',
        'db_alias': 'discogs',
        'indexes': [
            {'fields': ['$name', "$name_variations", "$aliases"],
             'default_language': 'english',
             'weights': {'name': 10, 'name_variations': 7, 'aliases': 7}
             }
        ]
    }

    discogs_id = IntField(unique=True)
    name = StringField()
    profile = StringField()
    real_name = StringField()
    data_quality = StringField()

    aliases = ListField(StringField())
    name_variations = ListField(StringField())
    members = EmbeddedDocumentListField(Member)
    groups = ListField(StringField())
    urls = ListField(StringField())

    @classmethod
    def init(cls, artist):
        """
        initialize ArtistDB Model from Artist Parser
        :param artist: artist instance (discogs_parser)
        :return: ArtistDB
        """

        artist_db = cls()
        artist_db.discogs_id = int(artist.id)
        artist_db.name = artist.name
        artist_db.profile = artist.profile
        artist_db.real_name = artist.realname
        artist_db.data_quality = artist.data_quality
        artist_db.aliases = artist.aliases
        artist_db.name_variations = artist.namevariations
        artist_db.members = list(map(Member.init, artist.members or []))
        artist_db.groups = artist.groups
        artist_db.urls = artist.urls

        return artist_db

    def make_json(self):
        return {
            "gid": str(self._id),
            "name": self.name,
            "profile": self.profile,
            "groups": self.groups,
            "real_name": self.real_name
        }

    def __str__(self):
        return f"<ArtistDB(id={self.id}, name={self.name})>"


class EmbeddedArtist(EmbeddedDocument):

    id = IntField()
    name = StringField()
    join = StringField()
    role = StringField()

    @classmethod
    def init(cls, artist):
        return cls(id=int(artist['id']),
                   name=artist['name'],
                   join=artist['join'],
                   role=artist['role'])

    def make_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role
        }

class EmbeddedCompany(EmbeddedDocument):

    entity_type = IntField()
    entity_type_name = StringField()
    id = IntField()
    name = StringField()

    @classmethod
    def init(cls, company):
        return cls(entity_type=company['entity_type'],
                   entity_type_name=company['entity_type_name'],
                   id=int(company['id']),
                   name=company['name'])

    def make_json(self):
        return {
            "entity_type": self.entity_type,
            "entity_type_name": self.entity_type_name,
            "id": self.id,
            "name": self.name
        }

class EmbeddedTrack(EmbeddedDocument):

    title = StringField()
    position = StringField()
    duration = StringField()

    @classmethod
    def init(cls, track):
        return cls(title=track['title'],
                   position=track['position'],
                   duration=track['duration'])

    def make_json(self):
        return {
            "title": self.title,
            "duration": self.duration
        }


class ReleaseDB(Document):

    meta = {
        'collection': 'releases',
        'db_alias': 'discogs',
        'indexes': [
        ]
    }

    discogs_id = IntField(unique=True)
    country = StringField()
    data_quality = StringField()
    title = StringField()
    notes = StringField()
    master_id = IntField()
    status = StringField()

    artists = EmbeddedDocumentListField(EmbeddedArtist)
    genres = ListField(StringField())
    styles = ListField(StringField())
    companies = EmbeddedDocumentListField(EmbeddedCompany)
    extra_artists = EmbeddedDocumentListField(EmbeddedArtist)
    track_list = EmbeddedDocumentListField(EmbeddedTrack)

    @classmethod
    def init(cls, release):
        """
        initialize ReleaseDB Model from Release Parser
        :param release: release instance (discogs_parser)
        :return: ReleaseDB
        """

        release_db = cls()
        release_db.discogs_id = int(release.id)
        release_db.country = release.country
        release_db.data_quality = release.data_quality
        release_db.title = release.title
        release_db.notes = release.notes
        release_db.status = release.status
        release_db.genres = release.genres
        release_db.styles = release.styles

        master_id = int(release.master_id) if release.master_id else None
        release_db.master_id = master_id

        release_db.artists = list(map(EmbeddedArtist.init, release.artists or []))
        release_db.companies = list(map(EmbeddedCompany.init, release.companies or []))
        release_db.extra_artists = list(map(EmbeddedArtist.init, release.extraartists or []))
        release_db.track_list = list(map(EmbeddedTrack.init, release.tracklist or []))

        return release_db

    def make_json(self):
        return {
            "gid": str(self._id),
            "country": self.country,
            "title": self.title,
            "artists": list(map(lambda x: x.make_json(), self.artists)),
            "genres": self.genres,
            "track_list": list(map(lambda x: x.make_json(), self.track_list))
            "styles": self.styles
        }

    def __str__(self):
        return f"<ReleaseDB(id={self.discogs_id}, title={self.title})>"



