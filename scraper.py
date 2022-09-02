import json
import datetime
from socket import timeout
from requests_html import HTMLSession
from http.client import responses

session = HTMLSession()


def linkCollect(url):
    try:
        response = session.get(url)
        response.html.render(sleep=1, timeout=20, scrolldown=10)

        # TODO: Add modularity here
        article = response.html.find('article')
        scrapelist = []

        for item in article:
            try:
                # TODO: Add modularity here
                newsitem = item.find('h3', first=True)
                linkitem = item.find('a', first=True)
                striplink = str(linkitem.absolute_links)

                newsdict = {
                    'Title': newsitem.text,
                    'Link': striplink.strip("{}''")
                }

                scrapelist.append(newsdict)
            except:
                pass
    except:
        print('Timeout Error in Link Collection')
        pass

    return scrapelist


def urlParse(source):
    urllist = linkCollect(source)

    length = len(urllist) + 1
    finalcontent = []

    for count, item in enumerate(urllist):
        cleaned = contentCollect(item['Link'], item['Title'], length, count)
        finalcontent.append(cleaned)

    return finalcontent


def contentCollect(parsedurl, parsedtitle, listlen, currentitem):
    try:
        response = session.get(parsedurl)
        response.html.render(sleep=1, timeout=20, scrolldown=0)
        # TODO: Add modularity here
        content = response.html.find('section')

        compile = []
        print('Article: ' + parsedtitle)
        print('Number ' + str(currentitem) + ' of ' + str(listlen))
        print('------')

        for index in content:
            try:
                # TODO: Add modularity here
                c = index.find('.zn-body__paragraph')
                for i in c:
                    res = i.text
                    compile.append(res)

                    while ('' in compile):
                        compile.remove('')

            except:
                print('Failed to parse paragraphs and append to list')
                pass
    except:
        print('Timeout Error in Content Collection')
        pass

    cleaned = {
        'Title': parsedtitle,
        'Link': parsedurl,
        'Content': compile
    }

    return cleaned


def main():
    # TODO: Add modularity here
    finalcontent = urlParse('https://www.cnn.com/world')

    with open('rawdata.json', 'w') as rawdataJSON:
        json.dump(finalcontent, rawdataJSON, indent=4)


if __name__ == '__main__':
    main()
