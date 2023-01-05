class Project:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Code:
    def __init__(self, codeId, name, color, projectId):
        self.id = codeId
        self.name = name
        self.color = color
        self.projectId = projectId
