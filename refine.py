import json
import re

from datetime import date


def findWord(word, string):
    if word in string:
        return True
    else:
        return False


def removeEmptyContent(rawdata):
    for index, value in enumerate(rawdata):
        content = value.get('Content')
        if not content:
            del rawdata[index]
        else:
            continue
    return rawdata


def removeBrand(data):
    for i in data:
        content = i.get('Content')
        for index, value in enumerate(content):
            match = re.search(r'\b(CNN)\b', value)
            if index == 0 and match:
                replaceword = '(' + match.group(0) + ')'
                value = value.replace(replaceword, '')
                del content[0]
                content.insert(index, value)
    return data


def removeContributor(data):
    for i in data:
        content = i.get('Content')
        for index, value in enumerate(content):
            if index == len(content)-1 and findWord('contributed', value):
                del content[index]
    return data


def main():
    with open('rawdata.json', 'r') as f:
        jsonfile = json.load(f)

    preclean = removeEmptyContent(jsonfile)
    nobrand = removeBrand(preclean)
    product = removeContributor(nobrand)

    today = date.today()
    filename = 'cleandata_' + str(today) + '.json'

    with open(filename, 'w') as writejson:
        json.dump(product, writejson, indent=4)


if __name__ == '__main__':
    main()
