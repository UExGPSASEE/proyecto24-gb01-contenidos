class Content:
    def __init__(self, title, urlVideo, releaseDate,
                 duration, language, category, character, participant):
        self.title = title
        self.duration = duration
        self.urlVideo = urlVideo
        self.language = language
        self.character = character
        self.participant = participant
        self.category = category
        self.releaseDate = releaseDate

    def toDBCollection(self):
        return {
            'title': self.title,
            'urlVideo': self.urlVideo,
            'releaseDate': self.releaseDate,
            'duration': self.duration,
            'language': self.language,
            'category': self.category,
            'character': self.character,
            'participant': self.participant,
        }
