class Category:
    def __init__(self, idCategory, name):
        self.idCategory = idCategory
        self.name = name

    def toDBCollection(self):
        return{
            'idCategory' : self.idCategory,
            'name' : self.name
        }