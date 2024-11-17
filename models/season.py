class Season:
    def __init__(self, idSeason, idSeries, title, seasonNumber, totalChapters,
                 chapterList, participants, trailer):
        self.idSeason = idSeason
        self.idSeries = idSeries
        self.title = title
        self.seasonNumber = seasonNumber
        self.totalChapters = totalChapters
        self.chapterList = chapterList
        self.participants = participants
        self.trailer = trailer

    def toDBCollection(self):
        return {
            'idSeason': self.idSeason,
            'idSeries': self.idSeries,
            'title': self.title,
            'seasonNumber': self.seasonNumber,
            'totalChapters': self.totalChapters,
            'chapterList': self.chapterList,
            'participants': self.participants,
            'trailer': self.trailer
        }
