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
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.html = ""

    def setName(self, name):
        self.name = name

    def setHtml(self, html):
        self.html = html

    def getHtml(self):
        return self.html

    def getId(self):
        return self.id


class CodeInstance:
    def __init__(self, text):
        self.text = text
        self.code = None
        self.start = None
        self.end = None
