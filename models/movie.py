class Movie:
    def __init__(self, idMovie, title, urlVideo, urlTitlePage, releaseDate, synopsis, description, 
                 isSuscription, duration, languages, categories, characters, participants, trailer):
        self.idMovie = idMovie
        self.title = title
        self.urlVideo = urlVideo
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
        return{
            'idMovie' : self.idMovie,
            'title' : self.title,
            'urlVideo' : self.urlVideo,
            'urlTitlePage' : self.urlTitlePage,
            'releaseDate' : self.releaseDate,
            'synopsis' : self.synopsis,
            'description' : self.description,
            'isSuscription' : self.isSuscription,
            'duration' : self.duration,
            'languages': self.languages,
            'categories': self.categories,
            'characters': self.characters,
            'participants': self.participants,
            'trailer' : self.trailer
        }