import json
from math import prod
from nltk.tag import pos_tag

article = ['A', 'An', 'The', 'There']
prepositions = ['At', 'As', 'For', 'In', 'On']
removal = ['Both', 'Article', 'Activist', 'Still', 'Medium', 'Department', 'Oval', 'Reduction', 'Office',
           'However', 'Spokesperson', 'Several', 'Opposition', 'Day', 'Sensitive', 'Through', 'DeirEzzor24', 'Deir', 'II', 'III', 'IV']
days = ['Monday', 'Tuesday', 'Wednesday',
        'Thursday', 'Friday', 'Saturday', 'Sunday']
months = ['January', 'Feburary', 'March', 'April', 'May',
          'June', 'July', 'August', 'October', 'November', 'December']


def concatContent(data):
    # TODO: Not returning all the text from the cleandata file. Why?
    catdata = []
    for i in data:
        content = i.get('Content')
        concat = ' '.join(content)
        catdata.append(concat)
    return catdata


def findProperNoun(data):
    fulllist = []
    for i in data:
        content = i.get('Content')
        concat = ' '.join(content)
        # Uses NLTK for Natural Language Processing to find the proper nouns
        tagged = pos_tag(concat.split())
        nounlist = [word for word, pos in tagged if pos ==
                    'NNP' or pos == 'NNPS']
        fulllist.append(nounlist)
    return fulllist

# Returns the "True" value of each element in the text list


def trueValue(value):
    trueval = value.translate({ord(c): None for c in '",.()[]'})
    return trueval


def compareValues(value, list):
    lowval = value.lower()
    for i in list:
        listval = i.lower()
        if lowval == listval:
            return True
        continue


def cleanNounList(data):
    transfer = []
    flatlist = []
    for lists in data:
        for items in lists:
            flatlist.append(items)

    cleanNouns = [*set(flatlist)]   # Not sure how this works but okay
    for index, value in enumerate(cleanNouns):
        truval = trueValue(value)
        # This could probably be made better
        if len(truval) < 0:
            cleanNouns.pop(index)
        if compareValues(truval, article):
            cleanNouns.pop(index)
        if compareValues(truval, prepositions):
            cleanNouns.pop(index)
        if compareValues(truval, removal):
            cleanNouns.pop(index)
        if compareValues(truval, days):
            cleanNouns.pop(index)
        if compareValues(truval, months):
            cleanNouns.pop(index)
        transfer.append(truval)
    return transfer


def main():
    with open('cleandata_2022-08-24.json', 'r') as f:
        jsonfile = json.load(f)

    # Collect Proper Nouns
    nouncollect = findProperNoun(jsonfile)
    product = cleanNounList(nouncollect)
    print(product)

    # Output text into training data txt file
    # concat = concatContent(jsonfile)

    # with open('concatdata.txt', 'a') as t:
    #     t.write(concat, t)


if __name__ == '__main__':
    main()
