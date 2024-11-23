from flask import Flask, render_template
from flask_cors import CORS

import database as dbase
from controllers.category_ctrl import CategoryCtrl
from controllers.chapter_ctrl import ChapterCtrl
from controllers.character_ctrl import CharacterCtrl
from controllers.movie_ctrl import MovieCtrl
from controllers.participant_ctrl import ParticipantCtrl
from controllers.season_ctrl import SeasonCtrl
from controllers.series_ctrl import SeriesCtrl
from controllers.trailer_ctrl import TrailerCtrl

db = dbase.conexionMongoDB()

app = Flask(__name__)

# CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # CORS restringido al origen React


# -------------------------------------------------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html')


# -------------------------------------------------------------------------------------------------------
@app.route('/movies')
def movies():
    return MovieCtrl.render_template(db['movies'])


@app.route('/movies', methods=['POST'])
def addMovie():
    return MovieCtrl.addMovie(db['movies'])


@app.route('/movies', methods=['DELETE'])
def deleteMovieForm():
    return MovieCtrl.deleteMovieForm(db['movies'])


@app.route('/movies/<idMovie>', methods=['DELETE'])
def deleteMovie(idMovie):
    return MovieCtrl.deleteMovie(db['movies'], idMovie)


@app.route('/movies', methods=['PUT'])
def putMovieForm():
    return MovieCtrl.putMovieForm(db['movies'])


@app.route('/movies/<idMovie>', methods=['PUT'])
def putMovie(idMovie):
    return MovieCtrl.putMovie(db['movies'], idMovie)


@app.route('/movies/<idMovie>', methods=['GET'])
def getMovieById(idMovie):
    return MovieCtrl.getMovieById(db['movies'], idMovie)


@app.route('/movies/title', methods=['GET'])
def getMovieByTitle():
    return MovieCtrl.getMovieByTitle(db['movies'])


@app.route('/movies/release', methods=['GET'])
def getMovieByReleaseDate():
    return MovieCtrl.getMovieByReleaseDate(db['movies'])


@app.route('/movies/all', methods=['GET'])
def getAllMovies():
    return MovieCtrl.getAllMovies(db['movies'])


@app.route('/movies/characters', methods=['GET'])
def getMovieCharacters():
    return MovieCtrl.getMovieCharacters(db['movies'], db['characters'])


@app.route('/movies/participants', methods=['GET'])
def getMovieParticipants():
    return MovieCtrl.getMovieParticipants(db['movies'], db['participants'])


# -------------------------------------------------------------------------------------------------------
@app.route('/trailers')
def trailers():
    return TrailerCtrl.render_template(db['trailers'])


@app.route('/trailers', methods=['POST'])
def addTrailer():
    return TrailerCtrl.addTrailer(db['trailers'])


@app.route('/trailers', methods=['DELETE'])
def deleteTrailerForm():
    return TrailerCtrl.deleteTrailerForm(db['trailers'])


@app.route('/trailers', methods=['PUT'])
def putTrailerForm():
    return TrailerCtrl.putTrailerForm(db['trailers'])


@app.route('/trailers/<idTrailer>', methods=['DELETE'])
def deleteTrailer(idTrailer):
    return TrailerCtrl.deleteTrailer(db['trailers'], idTrailer)


@app.route('/trailers/<idTrailer>', methods=['PUT'])
def putTrailer(idTrailer):
    return TrailerCtrl.putTrailer(db['trailers'], idTrailer)


@app.route('/trailers/<idTrailer>', methods=['GET'])
def getTrailerById(idTrailer):
    return TrailerCtrl.getTrailerById(db['trailers'], idTrailer)


# -------------------------------------------------------------------------------------------------------
@app.route('/chapters')
def chapters():
    return ChapterCtrl.render_template(db['chapters'])


@app.route('/chapters', methods=['POST'])
def addChapter():
    return ChapterCtrl.addChapter(db['chapters'])


@app.route('/chapters', methods=['DELETE'])
def deleteChapterForm():
    return ChapterCtrl.deleteChapterForm(db['chapters'])


@app.route('/chapters', methods=['PUT'])
def putChapterForm():
    return ChapterCtrl.putChapterForm(db['chapters'])


@app.route('/chapters/<idChapter>', methods=['DELETE'])
def deleteChapter(idChapter):
    return ChapterCtrl.deleteChapter(db['chapters'], idChapter)


@app.route('/chapters/<idChapter>', methods=['PUT'])
def putChapter(idChapter):
    return ChapterCtrl.putChapter(db['chapters'], idChapter)


@app.route('/chapters/<idChapter>', methods=['GET'])
def getChapterById(idChapter):
    return ChapterCtrl.getChapterById(db['chapters'], idChapter)


# -------------------------------------------------------------------------------------------------------

@app.route('/seasons')
def seasons():
    return SeasonCtrl.render_template(db['seasons'])


@app.route('/seasons', methods=['POST'])
def addSeason():
    return SeasonCtrl.addSeason(db['seasons'])


@app.route('/seasons', methods=['PUT'])
def putSeasonForm():
    return SeasonCtrl.putSeasonForm(db['seasons'])


@app.route('/seasons', methods=['DELETE'])
def deleteSeasonForm():
    return SeasonCtrl.deleteSeasonForm(db['seasons'])


@app.route('/seasons/<idSeason>', methods=['PUT'])
def putSeason(idSeason):
    return SeasonCtrl.putSeason(db['seasons'], idSeason)


@app.route('/seasons/<idSeason>', methods=['DELETE'])
def deleteSeason(idSeason):
    return SeasonCtrl.deleteSeason(db['seasons'], idSeason)


@app.route('/seasons/<idSeason>', methods=['GET'])
def getSeasonById(idSeason):
    return SeasonCtrl.getSeasonById(db['seasons'], idSeason)


@app.route('/seasons/chapters', methods=['GET'])
def getSeasonChapters():
    return SeasonCtrl.getSeasonChapters(db['seasons'], db['chapters'])


@app.route('/seasons/characters', methods=['GET'])
def getSeasonCharacters():
    return SeasonCtrl.getSeasonCharacters(db['seasons'], db['characters'])


@app.route('/seasons/participants', methods=['GET'])
def getSeasonParticipants():
    return SeasonCtrl.getSeasonParticipants(db['seasons'], db['participants'])


# -------------------------------------------------------------------------------------------------------

@app.route('/categories')
def categories():
    return CategoryCtrl.render_template(db['categories'])


@app.route('/categories', methods=['POST'])
def addCategory():
    return CategoryCtrl.addCategory(db['categories'])


@app.route('/categories/all', methods=['GET'])
def getAllCategories():
    return CategoryCtrl.getAllCategories(db['categories'])


@app.route('/categories/<idCategory>', methods=['GET'])
def getCategoryById(idCategory):
    return CategoryCtrl.getCategoryById(db['categories'], idCategory)


# No se borran ni se modifican categorías.

@app.route('/categories/content', methods=['GET'])
def getContentByCategory():
    return CategoryCtrl.getContentByCategory(db['categories'], db['movies'], db['series'])


# -------------------------------------------------------------------------------------------------------

@app.route('/participants')
def participants():
    return ParticipantCtrl.render_template(db['participants'])


@app.route('/participants', methods=['POST'])
def addParticipant():
    return ParticipantCtrl.addParticipant(db['participants'])


@app.route('/participants', methods=['PUT'])
def putParticipantForm():
    return ParticipantCtrl.putParticipantForm(db['participants'])


@app.route('/participants', methods=['DELETE'])
def deleteParticipantForm():
    return ParticipantCtrl.deleteParticipantForm(db['participants'])


@app.route('/participants/<idParticipant>', methods=['PUT'])
def putParticipant(idParticipant):
    return ParticipantCtrl.putParticipant(db['participants'], idParticipant)


@app.route('/participants/<idParticipant>', methods=['DELETE'])
def deleteParticipant(idParticipant):
    return ParticipantCtrl.deleteParticipant(db['participants'], idParticipant)


@app.route('/participants/<idParticipant>', methods=['GET'])
def getParticipantById(idParticipant):
    return ParticipantCtrl.getParticipantById(db['participants'], idParticipant)


@app.route('/participants/name', methods=['GET'])
def getParticipantByName():
    return ParticipantCtrl.getParticipantByName(db['participants'])


@app.route('/participants/surname', methods=['GET'])
def getParticipantBySurname():
    return ParticipantCtrl.getParticipantBySurname(db['participants'])


@app.route('/participants/age', methods=['GET'])
def getParticipantByAge():
    return ParticipantCtrl.getParticipantByAge(db['participants'])


@app.route('/participants/content', methods=['GET'])
def getContentByParticipant():
    return ParticipantCtrl.getContentByParticipant(db['participants'], db['movies'], db['series'])

@app.route('/participants/all', methods=['GET'])
def getAllParticipants():
    return ParticipantCtrl.getAllParticipants(db['participants'])


# -------------------------------------------------------------------------------------------------------

@app.route('/characters')
def characters():
    return CharacterCtrl.render_template(db['characters'])


@app.route('/characters', methods=['POST'])
def addCharacter():
    return CharacterCtrl.addCharacter(db['characters'])


@app.route('/characters', methods=['PUT'])
def putCharacterForm():
    return CharacterCtrl.putCharacterForm(db['characters'])


@app.route('/characters', methods=['DELETE'])
def deleteCharacterForm():
    return CharacterCtrl.deleteCharacterForm(db['characters'])


@app.route('/characters/<idCharacter>', methods=['PUT'])
def putCharacter(idCharacter):
    return CharacterCtrl.putCharacter(db['characters'], idCharacter)


@app.route('/characters/<idCharacter>', methods=['DELETE'])
def deleteCharacter(idCharacter):
    return CharacterCtrl.deleteCharacter(db['characters'], idCharacter)


@app.route('/characters/<idCharacter>', methods=['GET'])
def getCharacterById(idCharacter):
    return CharacterCtrl.getCharacterById(db['characters'], idCharacter)


@app.route('/characters/name', methods=['GET'])
def getCharacterByName():
    return CharacterCtrl.getCharacterByName(db['characters'])


@app.route('/characters/age', methods=['GET'])
def getCharacterByAge():
    return CharacterCtrl.getCharacterByAge(db['characters'])


@app.route('/characters/all', methods=['GET'])
def getAllCharacters():
    return CharacterCtrl.getAllCharacters(db['characters'])


@app.route('/characters/content', methods=['GET'])
def getContentByCharacter():
    return CharacterCtrl.getContentByCharacter(db['characters'], db['movies'], db['series'])


# -------------------------------------------------------------------------------------------------------

@app.route('/series')
def series():
    return SeriesCtrl.render_template(db['series'])


@app.route('/series', methods=['POST'])
def addSeries():
    return SeriesCtrl.addSeries(db['series'])


@app.route('/series/all', methods=['GET'])
def getAllSeries():
    return SeriesCtrl.getAllSeries(db['series'])


@app.route('/series/title', methods=['GET'])
def getSeriesByTitle():
    return SeriesCtrl.getSeriesByTitle(db['series'])


@app.route('/series/<idSeries>', methods=['GET'])
def getSeriesById(idSeries):
    return SeriesCtrl.getSeriesById(db['series'], idSeries)


@app.route('/series', methods=['DELETE'])
def deleteSeriesForm():
    return SeriesCtrl.deleteSeriesForm(db['series'])


@app.route('/series', methods=['PUT'])
def putSeriesForm():
    return SeriesCtrl.putSeriesForm(db['series'])


@app.route('/series/<idSeries>', methods=['DELETE'])
def deleteSeries(idSeries):
    return SeriesCtrl.deleteSeries(db['series'], idSeries)


@app.route('/series/<idSeries>', methods=['PUT'])
def putSeries(idSeries):
    return SeriesCtrl.putSeries(db['series'], idSeries)


@app.route('/series/chapters', methods=['GET'])
def getSeriesChapters():
    return SeriesCtrl.getSeriesChapters(db['series'], db['seasons'])


@app.route('/series/characters', methods=['GET'])
def getSeriesCharacters():
    return SeriesCtrl.getSeriesCharacters(db['series'], db['characters'])


@app.route('/series/participants', methods=['GET'])
def getSeriesParticipants():
    return SeriesCtrl.getSeriesParticipants(db['series'], db['participants'])


# -------------------------------------------------------------------------------------------------------

@app.route('/trailers/<idTrailer>/categories', methods=['PUT'])
def putCategoryIntoTrailer(idTrailer):
    return TrailerCtrl.putCategoryIntoTrailer(db['trailers'], db['categories'], idTrailer)


@app.route('/trailers/<idTrailer>/categories', methods=['DELETE'])
def deleteCategoryFromTrailer(idTrailer):
    return TrailerCtrl.deleteCategoryFromTrailer(db['trailers'], idTrailer)

@app.route('/movies/<idMovie>/trailer', methods=['PUT'])
def putTrailerIntoMovie(idMovie):
    return MovieCtrl.putTrailerIntoMovie(db['movies'], db['trailers'], idMovie)


@app.route('/movies/<idMovie>/trailer', methods=['DELETE'])
def deleteTrailerFromMovie(idMovie):
    return MovieCtrl.deleteTrailerFromMovie(db['movies'], idMovie)


# @app.route('/movies/<idMovie>/characters', methods=['PUT'])
# def putCharacterIntoMovie(idMovie):
#     return MovieCtrl.putCharacterIntoMovie(db['movies'], db['characters'], idMovie)
#
#
# @app.route('/movies/<idMovie>/characters', methods=['DELETE'])
# def deleteCharacterFromMovie(idMovie):
#     return MovieCtrl.putCharacterIntoMovie(db['movies'], idMovie)


@app.route('/movies/<idMovie>/categories', methods=['PUT'])
def putCategoryIntoMovie(idMovie):
    return MovieCtrl.putCategoryIntoMovie(db['movies'], db['categories'], idMovie)


@app.route('/movies/<idMovie>/categories', methods=['DELETE'])
def deleteCategoryFromMovie(idMovie):
    return MovieCtrl.deleteCategoryFromMovie(db['movies'], idMovie)

@app.route('/series/<idSeries>/trailer', methods=['PUT'])
def putTrailerIntoSeries(idSeries):
    return SeriesCtrl.putTrailerIntoSeries(db['series'], db['trailers'], idSeries)

@app.route('/series/<idSeries>/trailer', methods=['DELETE'])
def deleteTrailerFromSeries(idSeries):
    return SeriesCtrl.deleteTrailerFromSeries(db['series'], idSeries)

# @app.route('/series/<idSeries>/characters', methods=['PUT'])
# def putCharacterIntoSeries(idSeries):
#     return SeriesCtrl.putCharacterIntoSeries(db['series'], db['characters'], idSeries)
#
#
# @app.route('/series/<idSeries>/characters', methods=['DELETE'])
# def removeCharacterFromSeries(idSeries):
#     return SeriesCtrl.removeCharacterFromSeries(db['series'], idSeries)


@app.route('/series/<idSeries>/categories', methods=['PUT'])
def putCategoryIntoSeries(idSeries):
    return SeriesCtrl.putCategoryIntoSeries(db['series'], db['categories'], idSeries)


@app.route('/series/<idSeries>/categories', methods=['DELETE'])
def deleteCategoryFromSeries(idSeries):
    return SeriesCtrl.deleteCategoryFromSeries(db['series'], idSeries)

@app.route('/seasons/<idSeason>/trailer', methods=['PUT'])
def putTrailerIntoSeasons(idSeason):
    return SeasonCtrl.putTrailerIntoSeason(db['seasons'], db['trailers'], idSeason)

@app.route('/seasons/<idSeason>/trailer', methods=['DELETE'])
def deleteTrailerFromSeason(idSeason):
    return SeasonCtrl.deleteTrailerFromSeason(db['seasons'], idSeason)

# @app.route('/seasons/<idSeason>/characters', methods=['PUT'])
# def putCharacterIntoSeason(idSeason):
#     return SeasonCtrl.putCharacterIntoSeason(db['seasons'], db['characters'], idSeason)
#
#
# @app.route('/seasons/<idSeason>/characters', methods=['DELETE'])
# def deleteCharacterFromSeason(idSeason):
#     return SeasonCtrl.putCharacterIntoSeason(db['seasons'], idSeason)

@app.route('/seasons/<idSeason>/categories', methods=['PUT'])
def putCategoryIntoSeason(idSeason):
    return SeasonCtrl.putCategoryIntoSeason(db['seasons'], db['categories'], idSeason)


@app.route('/seasons/<idSeason>/categories', methods=['DELETE'])
def deleteCategoryFromSeason(idSeason):
    return SeasonCtrl.deleteCategoryFromSeason(db['seasons'], idSeason)
 

if __name__ == '__main__':
    app.run(debug=True, port=8082)
