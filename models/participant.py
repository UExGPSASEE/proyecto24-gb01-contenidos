class Participant:
    def __init__(self, participant_id, name, surname, age, nationality):
        self.participant_id = participant_id
        self.name = name
        self.surname = surname
        self.age = age
        self.nationality = nationality

    def toDBCollection(self):
        return {
            'participant_id' : self.participant_id,
            'name': self.name,
            'surname': self.surname,
            'age': self.age,
            'nationality': self.nationality
        }
