#!/usr/bin/env python

from lxml import html
import sys
import urllib
import getopt
import os
import threading2
from httplib2 import iri2uri
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

def download_track(url, filename):
    logging.debug( "Retriveing %s", filename)
    track, base = extract_base_and_track(url)
    url_to_download=base + bytes(iri2uri(track))
    urllib.urlretrieve(url_to_download, filename)


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
        logging.debug( "%s already exists in %s. Ignoring" % (filename, path))
        return True
    else:
        return False

def extract_base_and_track(url):
    idx = url.rfind('/')+1
    track = url[idx:]
    base = url[:idx]
    return (track, base)


def main():
    number_of_tracks = -1  # number of tracks to download
    path = os.curdir
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:p:", ["tracks=", "path="])
    except getopt.GetoptError as err:
        logging.debug( str(err))  # will logging.debug( something like "option -a not recognized"
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
    logging.debug( "Begin to retrieve %d tracks into %s" % (len(tracks_urls), path))
    threads = []
    for url in tracks_urls:
        track, base = extract_base_and_track(url)
        if check_for_existence(track, path) is False:
            filename = os.path.join(path, track)
            t = threading2.Thread(target=download_track, args=(url, filename))
            threads.append(t)
            t.start()
#            download_track(url, filename)

if __name__ == '__main__':
    main()
