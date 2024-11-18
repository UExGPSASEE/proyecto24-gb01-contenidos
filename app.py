import database as dbase
from flask import Flask, render_template, request, jsonify, redirect, url_for
from controllers.movie_ctrl import MovieCtrl
from controllers.category_ctrl import CategoryCtrl
from controllers.participant_ctrl import ParticipantCtrl
from controllers.trailer_ctrl import TrailerCtrl
from controllers.chapter_ctrl import ChapterCtrl
from controllers.series_ctrl import SeriesCtrl
from controllers.season_ctrl import SeasonCtrl
from controllers.character_ctrl import CharacterCtrl

db = dbase.conexionMongoDB()

app = Flask(__name__)
# -------------------------------------------------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html')
# -------------------------------------------------------------------------------------------------------
@app.route('/movies')
def movies():
    return MovieCtrl.render_template(db['movies'])

@app.route('/movies/addMovie', methods=['POST'])
def addMovie():
    return MovieCtrl.addMovie(db['movies'])

@app.route('/movies/deleteMovie', methods=['POST'])
def deleteMovie():
    return MovieCtrl.delete_movie(db['movies'])

@app.route('/movies/movieFound', methods=['GET'])
def getMovieById():
    return MovieCtrl.getMovieById(db['movies'])

@app.route('/movies/title', methods=['GET'])
def getMovieByTitle():
    return MovieCtrl.getMovieByTitle(db['movies'])

@app.route('/movies/release', methods=['GET'])
def getMovieByReleaseDate():
    return MovieCtrl.getMovieByReleaseDate(db['movies'])

@app.route('/movies/all', methods=['GET'])
def getAllMovies():
    return MovieCtrl.getAllMovies(db['movies'])

@app.route('/movies/updateMovie', methods=['POST'])
def putMovie():
    return MovieCtrl.put_movie(db['movies'])

# -------------------------------------------------------------------------------------------------------
@app.route('/trailers')
def trailers():
    return TrailerCtrl.render_template(db['trailers'])

@app.route('/trailers/addTrailer', methods=['POST'])
def addTrailer():
    return TrailerCtrl.addTrailer(db['trailers'])

@app.route('/trailers/deleteTrailer', methods=['POST'])
def deleteTrailer():
    return TrailerCtrl.delete_trailer(db['trailers'])

@app.route('/trailers/updateTrailer', methods=['POST'])
def putTrailer():
    return TrailerCtrl.put_trailer(db['trailers'])

# @app.route('/trailers/trailerFound', methods=['GET'])
# def getTrailerById():
#     return TrailerCtrl.getTrailerById(db['trailers'])

# -------------------------------------------------------------------------------------------------------
@app.route('/chapters')
def chapters():
    return ChapterCtrl.render_template(db['chapters'])

@app.route('/chapters/addChapter', methods=['POST'])
def addChapter():
    return ChapterCtrl.addChapter(db['chapters'])

@app.route('/chapters/deleteChapter', methods=['POST'])
def deleteChapter():
    return ChapterCtrl.delete_chapter(db['chapters'])

@app.route('/chapters/updateChapter', methods=['POST'])
def putChapter():
    return ChapterCtrl.put_chapter(db['chapters'])

@app.route('/chapters/chapterFound', methods=['GET'])
def getChapterById():
    return ChapterCtrl.getChapterById(db['chapters'])

# -------------------------------------------------------------------------------------------------------

@app.route('/seasons')
def seasons():
    return SeasonCtrl.render_template(db['seasons'])

@app.route('/seasons/addSeason', methods=['POST'])
def addSeason():
    return SeasonCtrl.addSeason(db['seasons'])

@app.route('/seasons/updateSeason', methods=['POST'])
def putSeason():
    return SeasonCtrl.put_season(db['seasons'])

@app.route('/seasons/deleteSeason', methods=['POST'])
def deleteSeason():
    return SeasonCtrl.delete_season(db['seasons'])

@app.route('/seasons/seasonFound', methods=['GET'])
def getSeasonById():
    return SeasonCtrl.getSeasonById(db['seasons'])

# -------------------------------------------------------------------------------------------------------

@app.route('/categories')
def categories():
    return CategoryCtrl.render_template(db['categories'])

@app.route('/categories/categoryAdded', methods=['POST'])
def addCategory():
    return CategoryCtrl.addCategory(db['categories'])

@app.route('/categories/categoriesListed', methods=['GET'])
def getAllCategories():
    return CategoryCtrl.getAllCategories(db['categories'])

@app.route('/categories/categoryFound', methods=['GET'])
def getCategoryById():
    return CategoryCtrl.getCategoryById(db['categories'])

# -------------------------------------------------------------------------------------------------------

@app.route('/participants')
def participants():
    return ParticipantCtrl.render_template(db['participants'])

@app.route('/participants/addParticipant', methods=['POST'])
def addParticipant():
    return ParticipantCtrl.addParticipant(db['participants'])

@app.route('/participants/updateParticipant', methods=['POST'])
def updateParticipant():
    return ParticipantCtrl.updateParticipant(db['participants'])

@app.route('/participants/deleteParticipant', methods=['POST'])
def deleteParticipant():
    return ParticipantCtrl.deleteParticipant(db['participants'])

@app.route('/participants/getParticipantByName', methods=['GET'])
def getParticipantByName():
    return ParticipantCtrl.getParticipantByName(db['participants'])

@app.route('/participants/getParticipantBySurname', methods=['GET'])
def getParticipantBySurname():
    return ParticipantCtrl.getParticipantBySurname(db['participants'])

@app.route('/participants/getParticipantByAge', methods=['GET'])
def getParticipantByAge():
    return ParticipantCtrl.getParticipantByAge(db['participants'])

@app.route('/participants/getParticipantById', methods=['GET'])
def getParticipantById():
    return ParticipantCtrl.getParticipantById(db['participants'])

@app.route('/participants/getAllParticipants', methods=['GET'])
def getAllParticipants():
    return ParticipantCtrl.getAllParticipants(db['participants'])

# -------------------------------------------------------------------------------------------------------

@app.route('/characters')
def characters():
    return CharacterCtrl.render_template(db['characters'])

@app.route('/characters/addCharacter', methods=['POST'])
def addCharacter():
    return CharacterCtrl.addCharacter(db['characters'])

@app.route('/characters/updateCharacter', methods=['POST'])
def updateCharacter():
    return CharacterCtrl.updateCharacter(db['characters'])

@app.route('/characters/deleteCharacter', methods=['POST'])
def deleteCharacter():
    return CharacterCtrl.deleteCharacter(db['characters'])


@app.route('/characters/getCharacterByName', methods=['GET'])
def getCharacterByName():
    return CharacterCtrl.getCharacterByName(db['characters'])

@app.route('/characters/getCharacterByAge', methods=['GET'])
def getCharacterByAge():
    return CharacterCtrl.getCharacterByAge(db['characters'])

@app.route('/characters/getCharacterById', methods=['GET'])
def getCharacterById():
    return CharacterCtrl.getCharacterById(db['characters'])

@app.route('/characters/getAllCharacters', methods=['GET'])
def getAllCharacters():
    return CharacterCtrl.getAllCharacters(db['characters'])

# -------------------------------------------------------------------------------------------------------

@app.route('/series')
def series():
    return SeriesCtrl.render_template(db['series'])

@app.route('/series/addSeries', methods=['POST'])
def addSeries():
    return SeriesCtrl.addSeries(db['series'])

@app.route('/series/deleteSeries', methods=['POST'])
def deleteSeries():
    return SeriesCtrl.delete_series(db['series'])

@app.route('/series/updateSeries', methods=['POST'])
def updateSeries():
    return SeriesCtrl.put_series(db['series'])

if __name__ == '__main__':
    app.run(debug=True, port=8082)
