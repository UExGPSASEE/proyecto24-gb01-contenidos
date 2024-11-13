class Participant:
    def __init__(self, name, surname, age, nationality):
        self.name = name
        self.surname = surname
        self.age = age
        self.nationality = nationality

    def toDBCollection(self):
        return {
            'name': self.name,
            'surname': self.surname,
            'age': self.age,
            'nationality': self.nationality
        }
