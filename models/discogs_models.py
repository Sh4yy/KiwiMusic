from mongoengine import *


class Members(EmbeddedDocument):

    id = IntField()
    name = StringField()

    @classmethod
    def init(cls, members):
        """
        initialize Members model from Members dict
        :param members: members dict
        :return: members model
        """
        return cls(id=int(members['id']),
                   name=members['name'])


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
    members = EmbeddedDocumentListField(Members)
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
        artist_db.members = list(map(Members.init, artist.members or []))
        artist_db.groups = artist.groups
        artist_db.urls = artist.urls

        return artist_db

    def __str__(self):
        return f"<ArtistDB(id={self.id}, name={self.name})>"
