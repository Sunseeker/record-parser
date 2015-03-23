from lxml import html
import urllib


def main():
    url="http://www.radiorecord.ru/radio/charts/"
    xpath_selector='//*[@id="page-superchart"]/div[@class="all_audio"]/article[@class="track-holder"]/div[@class="player-raiting-holder"]/div[@class="player_wrapper"]/table[@class="player"]/tr/td[@class="play_pause"]/@item_url'

    page = html.parse(url)
    tracks_urls = page.xpath(xpath_selector)
    for url in tracks_urls[:3]:
        idx = url.rfind('/')
        filename = url[idx+1:]
        print "Retriveing ", filename
        urllib.urlretrieve(url, filename)


if __name__ == '__main__':
    main()

