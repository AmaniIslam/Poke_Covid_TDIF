import re
import math
from collections import Counter

def clean(content):
    x = re.sub(r'\bhttps?://\S+\b', '', content)
    x = re.sub(r'[^\w\s]', '', x)
    x = x.split()
    x = ' '.join(x)
    x = x.lower()
    return x

def stop(content):
    with open("stopwords.txt", 'r') as file:
        words = file.read()
        words = words.split()
        x = content.split()
        x = [word for word in x if word not in words]
        x = ' '.join(x)
        return x

def stem(content):
    x = re.sub(r'(ly|ing|ment)\b','',content)
    return x

def tf(content, wordCount):
    words = content.split()

    countDict = dict(Counter(words))
    total = sum(countDict.values())

    tfDict = {}
    for key,value in countDict.items():
        if key in wordCount.keys():
            wordCount[key] += 1
        else:
            wordCount[key] = 1

        tfDict[key] = value/total
    return wordCount, tfDict

def idf(wordCount,lines):
    iDict = {}
    for key,value in wordCount.items():
        iDict[key] = math.log(lines/value) + 1

    return iDict

def diff(docDicts, iDict):
    for key, value in docDicts.items():
        for key2, value2 in value.items():
            docDicts[key][key2] = round(iDict[key2]*value2, 2)
        docDicts[key] = sorted(docDicts[key].items(), key=lambda x: x[1], reverse=True)

    return docDicts
    


def main():
    with open("tfidf_docs.txt", 'r') as file:
        content = file.read()
        lines = content.splitlines()
        num = len(lines)
        wordCount = {}
        docDicts = {}

        for line in lines:
            line = line.strip("\n")
            with open(line, 'r') as sub:
                contents = sub.read()
                result = clean(contents)
                result = stop(result)
                result = stem(result)
                with open('preproc_'+line, 'w+') as output:
                    output.write(result)
                    output.seek(0)
                    contents = output.read()
                    wordCount, tfDoc = tf(contents, wordCount)
                    docDicts[line] = tfDoc

        idfs = idf(wordCount, num)
        difDicts = diff(docDicts,idfs)
        for key, value in difDicts.items():
            five = value[:5]
            with open('tfidf_'+key, 'w') as out:
                out.write(str(five))

main()