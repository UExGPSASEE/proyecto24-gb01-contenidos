class Trailer:
    def __init__(self, idMovie, title, urlVideo,
                 duration, language, category, character, participant):
        self.idMovie = idMovie
        self.title = title
        self.urlVideo = urlVideo
        self.duration = duration
        self.language = language
        self.category = category
        self.character = character
        self.participant = participant

    def toDBCollection(self):
        return {
            'idMovie': self.idMovie,
            'title': self.title,
            'urlVideo': self.urlVideo,
            'duration': self.duration,
            'language': self.language,
            'category': self.category,
            'character': self.character,
            'participant': self.participant
        }
