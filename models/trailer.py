class Trailer:
    def __init__(self, id_trailer, title, url_video,
                 duration, languages, categories, characters, participants):
        self.id_trailer = id_trailer
        self.title = title
        self.url_video = url_video
        self.duration = duration
        self.languages = languages
        self.categories = categories
        self.characters = characters
        self.participants = participants

    def to_db_collection(self):
        return {
            'id_trailer': self.id_trailer,
            'title': self.title,
            'url_video': self.url_video,
            'duration': self.duration,
            'languages': self.languages,
            'categories': self.categories,
            'characters': self.characters,
            'participants': self.participants
        }
