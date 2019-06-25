from parsers.discogs_parser import Artist, Release, Master, Parser
from pprint import pprint
from models.discogs_models import ArtistDB, ReleaseDB, Document
from app import init_discogs_db


def update_discogs_db(file_path, db, parser, dump_every=100000):

    cache = []
    for index, item in enumerate(parser.parse(file_path)):
        cache.append(db.init(item))
        print(index)
        if index % dump_every == 0:
            db.objects.insert(cache)
            cache.clear()

    db.objects.insert(cache)


def main():

    init_discogs_db()

    artists_file = "discogs_20190601_artists.xml"
    masters_file = "discogs_20190601_masters.xml"
    releases_file = "discogs_20190601_releases.xml"

    ReleaseDB.objects.delete()
    update_discogs_db(file_path=f"data/{releases_file}",
                      db=ReleaseDB, parser=Release)


if __name__ == '__main__':
    main()