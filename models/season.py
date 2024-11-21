class Season:
    def __init__(self, idSeason, idSeries, title, seasonNumber, totalChapters,
                 chapterList, character, participant, trailer):
        self.idSeason = idSeason
        self.idSeries = idSeries
        self.title = title
        self.seasonNumber = seasonNumber
        self.totalChapters = totalChapters
        self.chapterList = chapterList
        self.character = character
        self.participant = participant
        self.trailer = trailer

    def toDBCollection(self):
        return {
            'idSeason': self.idSeason,
            'idSeries': self.idSeries,
            'title': self.title,
            'seasonNumber': self.seasonNumber,
            'totalChapters': self.totalChapters,
            'chapterList': self.chapterList,
            'character': self.character,
            'participant': self.participant,
            'trailer': self.trailer
        }
