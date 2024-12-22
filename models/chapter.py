class Chapter:
    def __init__(self, id_chapter, title, url_video,
                 duration, chapter_number):
        self.id_chapter = id_chapter
        self.title = title
        self.url_video = url_video
        self.duration = duration
        self.chapter_number = chapter_number

    def to_db_collection(self):
        return {
            'id_chapter': self.id_chapter,
            'title': self.title,
            'url_video': self.url_video,
            'duration': self.duration,
            'chapter_number': self.chapter_number
        }
