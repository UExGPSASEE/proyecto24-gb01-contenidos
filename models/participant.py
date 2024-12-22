class Participant:
    def __init__(self, id_participant, name, surname, age, nationality):
        self.id_participant = id_participant
        self.name = name
        self.surname = surname
        self.age = age
        self.nationality = nationality

    def to_db_collection(self):
        return {
            'id_participant': self.id_participant,
            'name': self.name,
            'surname': self.surname,
            'age': self.age,
            'nationality': self.nationality
        }
