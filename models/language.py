class Language:
    def __init__(self, idLanguage, name):
        self.idLanguage = idLanguage
        self.name = name

    def toDBCollection(self):
        return {
            'idLanguage': self.idLanguage,
            'name': self.name
        }