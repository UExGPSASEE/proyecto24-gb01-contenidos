import database as dbase
from flask import Flask, render_template, request, jsonify, redirect, url_for
from controllers.movie_ctrl import MovieCtrl
from controllers.category_ctrl import CategoryCtrl
from controllers.participant_ctrl import ParticipantCtrl
from controllers.trailer_ctrl import TrailerCtrl
from controllers.chapter_ctrl import ChapterCtrl
from controllers.serie_ctrl import SerieCtrl
from controllers.season_ctrl import SeasonCtrl

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

# @app.route('/chapters/chapterFound', methods=['GET'])
# def getChapterById():
#     return ChapterCtrl.getChapterById(db['chapters'])

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

# @app.route('/seasons/seasonFound', methods=['GET'])
# def getSeasonById():
#     return SeasonCtrl.getSeasonById(db['seasons'])

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

@app.route('/participants/getParticipantByName', methods=['GET'])
def getParticipantByName():
    return ParticipantCtrl.getParticipantByName(db['participants'])

@app.route('/participants/getParticipantBySurname', methods=['GET'])
def getParticipantBySurname():
    return ParticipantCtrl.getParticipantBySurname(db['participants'])

@app.route('/participants/getParticipantByAge', methods=['GET'])
def getParticipantByAge():
    return ParticipantCtrl.getParticipantByAge(db['participants'])

@app.route('/participants/getParticipantByNationality', methods=['GET'])
def getParticipantByNationality():
    return ParticipantCtrl.getParticipantByNationality(db['participants'])

@app.route('/participants/getParticipantById', methods=['GET'])
def getParticipantById():
    return ParticipantCtrl.getParticipantById(db['participants'])

@app.route('/participants/getAllParticipants', methods=['GET'])
def getAllParticipants():
    return ParticipantCtrl.getAllParticipants(db['participants'])

@app.route('/participants/updateParticipant', methods=['POST'])
def updateParticipant():
    return ParticipantCtrl.updateParticipant(db['participants'])

@app.route('/participants/deleteParticipant', methods=['POST'])
def deletePerticipant():
    return ParticipantCtrl.deleteParticipant(db['participants'])

# -------------------------------------------------------------------------------------------------------

@app.route('/series')
def series():
    return SerieCtrl.render_template(db['series'])

@app.route('/series/addSerie', methods=['POST'])
def addSerie():
    return SerieCtrl.addSerie(db['series'])

if __name__ == '__main__':
    app.run(debug=True, port=8082)
