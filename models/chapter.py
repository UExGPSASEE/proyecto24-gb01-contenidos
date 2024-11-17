class Chapter:
    def __init__(self, idChapter, title, urlVideo,
                 duration, chapterNumber):
        self.idChapter = idChapter
        self.title = title
        self.urlVideo = urlVideo
        self.duration = duration
        self.chapterNumber = chapterNumber

    def toDBCollection(self):
        return {
            'idChapter': self.idChapter,
            'title': self.title,
            'urlVideo': self.urlVideo,
            'duration': self.duration,
            'chapterNumber': self.chapterNumber
        }
