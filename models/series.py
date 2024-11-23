class Series:
    def __init__(self, idSeries, title, seasons, urlTitlePage, releaseDate, synopsis, description,
                 isSuscription, duration, languages, categories, characters, participants, trailer):
        self.idSeries = idSeries
        self.title = title
        self.seasons = seasons
        self.urlTitlePage = urlTitlePage
        self.releaseDate = releaseDate
        self.synopsis = synopsis
        self.description = description
        self.isSuscription = isSuscription
        self.duration = duration
        self.languages = languages
        self.categories = categories
        self.characters = characters
        self.participants = participants
        self.trailer = trailer

    def toDBCollection(self):
        return {
            'idSeries': self.idSeries,
            'title': self.title,
            'seasons': self.seasons,
            'urlTitlePage': self.urlTitlePage,
            'releaseDate': self.releaseDate,
            'synopsis': self.synopsis,
            'description': self.description,
            'isSuscription': self.isSuscription,
            'duration': self.duration,
            'languages': self.languages,
            'categories': self.categories,
            'characters': self.characters,
            'participants': self.participants,
            'trailer': self.trailer
        }
