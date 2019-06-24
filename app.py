from mongoengine import connect
from config import get_config


def init_discogs_db():
    connect("discogs",
            host=get_config()['databases']['discogs']['mongodb']['url'],
            alias="discogs")
