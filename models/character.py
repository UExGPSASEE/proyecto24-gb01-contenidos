class Character:
    def __init__(self, id_character, name, participant, age):
        self.id_character = id_character
        self.name = name
        self.participant = participant
        self.age = age

    def to_db_collection(self):
        return {
            'id_character': self.id_character,
            'name': self.name,
            'participant': self.participant,
            'age': self.age,
        }
