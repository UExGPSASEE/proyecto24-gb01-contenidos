class Trailer:
    def __init__(self, idTrailer, title, urlVideo,
                 duration, languages, categories, characters, participants):
        self.idTrailer = idTrailer
        self.title = title
        self.urlVideo = urlVideo
        self.duration = duration
        self.languages = languages
        self.categories = categories
        self.characters = characters
        self.participants = participants

    def toDBCollection(self):
        return {
            'idTrailer': self.idTrailer,
            'title': self.title,
            'urlVideo': self.urlVideo,
            'duration': self.duration,
            'languages': self.languages,
            'categories': self.categories,
            'characters': self.characters,
            'participants': self.participants
        }
