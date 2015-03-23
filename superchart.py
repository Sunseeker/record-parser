#!/usr/bin/python

import sys
from lxml import html
import requests


def get_track_list():
    page = requests.get("http://www.radiorecord.ru/radio/charts/")
    tree = html.fromstring(page.text)
    tracks = tree.xpath('//*[@id="page-superchart"]/div[3]')
    return tracks

def download_track():
    pass

def main():
    tracks = get_track_list(body)
    print tracks
#    for track in tracks:
#        download_track(track)
#    print 'Hello world!'

if __name__ == '__main__':
    main()

