class Movie:
    def __init__(self, id_movie, title, url_video, url_title_page, release_date, synopsis, description, 
                 is_subscription, duration, languages, categories, characters, participants, trailer):
        self.id_movie = id_movie
        self.title = title
        self.url_video = url_video
        self.url_title_page = url_title_page
        self.release_date = release_date
        self.synopsis = synopsis
        self.description = description
        self.is_subscription = is_subscription
        self.duration = duration
        self.languages = languages
        self.categories = categories
        self.characters = characters
        self.participants = participants
        self.trailer = trailer

    def to_db_collection(self):
        return{
            'id_movie' : self.id_movie,
            'title' : self.title,
            'url_video' : self.url_video,
            'url_title_page' : self.url_title_page,
            'release_date' : self.release_date,
            'synopsis' : self.synopsis,
            'description' : self.description,
            'is_subscription' : self.is_subscription,
            'duration' : self.duration,
            'languages': self.languages,
            'categories': self.categories,
            'characters': self.characters,
            'participants': self.participants,
            'trailer' : self.trailer
        }