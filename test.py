from parsers.discogs_parser import Artist, Release, Master
from pprint import pprint


def main():

    artists_file = "discogs_20190601_artists.xml"
    masters_file = "discogs_20190601_masters.xml"
    releases_file = "discogs_20190601_releases.xml"

    for index, artist in enumerate(Artist.parse(f'data/{artists_file}')):
        pprint(artist.__dict__)
        if index == 0:
            break

    for index, release in enumerate(Release.parse(f'data/{releases_file}')):
        pprint(release.__dict__)
        if index == 0:
            break

    for index, master in enumerate(Master.parse(f'data/{masters_file}')):
        pprint(master.__dict__)
        if index == 0:
            break



if __name__ == '__main__':
    main()