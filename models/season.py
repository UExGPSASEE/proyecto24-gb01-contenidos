class Season:
    def __init__(self, id_season, id_series, title, season_number, total_chapters,
                 chapters, characters, participants, trailer):
        self.id_season = id_season
        self.id_series = id_series
        self.title = title
        self.season_number = season_number
        self.total_chapters = total_chapters
        self.chapters = chapters
        self.characters = characters
        self.participants = participants
        self.trailer = trailer

    def to_db_collection(self):
        return {
            'id_season': self.id_season,
            'id_series': self.id_series,
            'title': self.title,
            'season_number': self.season_number,
            'total_chapters': self.total_chapters,
            'chapters': self.chapters,
            'characters': self.characters,
            'participants': self.participants,
            'trailer': self.trailer
        }
