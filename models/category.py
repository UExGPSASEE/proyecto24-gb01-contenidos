class Category:
    def __init__(self, id_category, name):
        self.id_category = id_category
        self.name = name

    def to_db_collection(self):
        return {
            'id_category': self.id_category,
            'name': self.name
        }
