from enum import Enum


class Project:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Code:
    def __init__(self, id, name, color):
        self.id = id
        self.name = name
        self.color = color


class Document:
    def __init__(self, id, name, text):
        self.id = id
        self.name = name
        self.text = text

    def setName(self, name):
        self.name = name

    def setHtml(self, html):
        self.html = html

    def getHtml(self):
        return self.html

    def getId(self):
        return self.id


class Category:
    def __init__(self, categoryId, name):
        self.id = categoryId
        self.name = name


class CodeInstance:
    def __init__(self, id, text, start, end, sentiment, code):
        self.id = id
        self.text = text
        self.start = start
        self.end = end
        self.sentiment = sentiment
        self.code = code

    def toString(self):
        print(self.text + ' start: ' + str(self.start) + ' end: ' + str(self.end) + '\n')


class Sentiment(Enum):
    NEUTRAL = 0
    POSITIVE = 1
    NEGATIVE = 2
