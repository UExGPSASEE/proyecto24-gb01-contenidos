class Character:
    def __init__(self, idCharacter, name, participant, age):
        self.idCharacter = idCharacter
        self.name = name
        self.participant = participant
        self.age = age

    def toDBCollection(self):
        return {
            'idCharacter' : self.idCharacter,
            'name': self.name,
            'participant': self.participant,
            'age': self.age,
        }
