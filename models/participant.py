class Participant:
    def __init__(self, idParticipant, name, surname, age, nationality):
        self.idParticipant = idParticipant
        self.name = name
        self.surname = surname
        self.age = age
        self.nationality = nationality

    def toDBCollection(self):
        return {
            'idParticipant' : self.idParticipant,
            'name': self.name,
            'surname': self.surname,
            'age': self.age,
            'nationality': self.nationality
        }
