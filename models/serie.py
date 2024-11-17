class Serie:
    def __init__(self, idSerie, title, seasons, urlTitlePage, releaseDate, synopsis, description,
                 isSuscription, duration, language, category, character, participant, trailer):
        self.idSerie = idSerie
        self.title = title
        self.seasons = seasons
        self.urlTitlePage = urlTitlePage
        self.releaseDate = releaseDate
        self.synopsis = synopsis
        self.description = description
        self.isSuscription = isSuscription
        self.duration = duration
        self.language = language
        self.category = category
        self.character = character
        self.participant = participant
        self.trailer = trailer

    def toDBCollection(self):
        return{
            'idSerie' : self.idSerie,
            'title' : self.title,
            'seasons' : self.seasons,
            'urlTitlePage' : self.urlTitlePage,
            'releaseDate' : self.releaseDate,
            'synopsis' : self.synopsis,
            'description' : self.description,
            'isSuscription' : self.isSuscription,
            'duration' : self.duration,
            'language' : self.language,
            'category' : self.category,
            'character' : self.character,
            'participant' : self.participant,
            'trailer' : self.trailer
        }
