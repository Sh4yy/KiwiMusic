from parsers.discogs_parser import Artist, Release, Master, Parser
from pprint import pprint
from models.discogs_models import ArtistDB, ReleaseDB, Document
from app import init_discogs_db
from threading import Thread, Lock


def update_discogs_db(file_path, db, parser):

    cache = []
    lock = Lock()
    work = True

    def parse_help():
        global work
        for index, item in enumerate(parser.parse(file_path)):
            if index % 200000 == 0:
                print(index)
            with lock:
                try:
                    cache.append(db.init(item))
                except Exception as e:
                    print(e)
        work = False

    def insert_help():
        while work or len(cache) > 0:
            if len(cache) > 0:
                with lock:
                    print('adding')
                    try:
                        db.objects.insert(cache)
                    except Exception as e:
                        print(e)
                    cache.clear()
        print('done')

    thread = Thread(target=parse_help)
    thread.start()
    insert_help()
    thread.join()


def main():

    init_discogs_db()
    print("connected")

    artists_file = "discogs_20190601_artists.xml"
    masters_file = "discogs_20190601_masters.xml"
    releases_file = "discogs_20190601_releases.xml"

    ReleaseDB.objects.delete()
    update_discogs_db(file_path=f"data/{releases_file}",
                      db=ReleaseDB, parser=Release)


if __name__ == '__main__':
    main()