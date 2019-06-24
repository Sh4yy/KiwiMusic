from parsers.discogs_parser import Artist, Release, Master
from pprint import pprint
from models.discogs_models import ArtistDB as ArtistDB
from app import init_discogs_db
from time import time

def main():

    init_discogs_db()

    artists_file = "discogs_20190601_artists.xml"
    masters_file = "discogs_20190601_masters.xml"
    releases_file = "discogs_20190601_releases.xml"

    # print(ArtistDB.objects)
    # ArtistDB.objects.delete()

    # cache = []
    # for index, artist in enumerate(Artist.parse(f'data/{artists_file}')):
    #     cache.append(ArtistDB.init(artist))
    #     print(index)
    #     if index % 100000 == 0:
    #         ArtistDB.objects.insert(cache)
    #         cache.clear()
    #         print("finished inserting")
    #
    # ArtistDB.objects.insert(cache)

    data = ArtistDB.objects.search_text('jack').order_by('$text_score')

    st = time()
    data = ArtistDB.objects.search_text('billie eilish').order_by('$text_score')
    # for item in data:
    #     print(item)
    print((time() - st))

    # for index, release in enumerate(Release.parse(f'data/{releases_file}')):
    #     pprint(release.__dict__)
    #     if index == 0:
    #         break
    #
    # for index, master in enumerate(Master.parse(f'data/{masters_file}')):
    #     pprint(master.__dict__)
    #     if index == 0:
    #         break



if __name__ == '__main__':
    main()