#!/usr/bin/env python

from lxml import html
import sys
import urllib
import getopt
import os


def download_track(url, filename):
    print "Retriveing ", filename
    urllib.urlretrieve(url, filename)


def get_tracks_urls():
    url = "http://www.radiorecord.ru/radio/charts/"
    xpath_selector = '//*[@class="play_pause"]/@item_url'
    page = html.parse(url)
    return page.xpath(xpath_selector)


def check_for_existence(filename, path=None):
    if path is None:
        path = os.curdir
    file_to_check = os.path.join(path, filename)
    if os.path.exists(file_to_check):
        print "%s already exists in %s. Ignoring" % (filename, path)
        return True
    else:
        return False


def main():
    number_of_tracks = -1  # number of tracks to download
    path = os.curdir
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:p:", ["tracks=", "path="])
    except getopt.GetoptError as err:
        print str(err)  # will print something like "option -a not recognized"
        sys.exit(2)
    for opts, args in opts:
        if opts in ("-t", "--tracks"):
            number_of_tracks = args
        elif opts in ("-p", "--path"):
            path = args
        else:
            assert False, "unhandled option"

    tracks_urls = get_tracks_urls()
    if number_of_tracks != -1:
        tracks_urls = tracks_urls[:int(number_of_tracks)]
    print "Begin to retrieve %d tracks" % len(tracks_urls)
    for url in tracks_urls:
        idx = url.rfind('/')+1
        track_name = url[idx:]
        filename = os.path.join(path, track_name)
        if check_for_existence(filename) is False:
            download_track(url, track_name)

if __name__ == '__main__':
    main()
