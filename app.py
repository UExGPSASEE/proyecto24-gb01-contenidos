import database as dbase
from flask import Flask, render_template, request, jsonify, redirect, url_for
from controllers.movie_ctrl import MovieCtrl
from category import Category
from participant import Participant

db = dbase.conexionMongoDB()

app = Flask(__name__)
# -------------------------------------------------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html')
# -------------------------------------------------------------------------------------------------------
@app.route('/movies')
def movies():
    movies = db['movies']
    moviesReceived = movies.find()
    return render_template('Movie.html', movies=moviesReceived)

@app.route('/movies/addMovie', methods=['POST'])
def addMovie():
    return MovieCtrl.addMovie(db['movies'])

@app.route('/movies/deleteMovie', methods=['POST'])
def deleteMovie():
    return MovieCtrl.delete_movie(db['movies'])

@app.route('/movies/movieFound', methods=['GET'])
def getMovieById():
    return MovieCtrl.getMovieById(db['movies'])
# -------------------------------------------------------------------------------------------------------
@app.route('/movies/put/<string:movies_name>', methods=['PUT'])
def putMovie(movie_name):
    movies = db['movies']
    name = request.form['name']

    if name:
        movies.update_one({'name': movie_name}, {'$set': {'name': name}})
        response = jsonify({'message': 'Movie' + movie_name + 'updated.'})
        return redirect(url_for('home'))
    else:
        return notFound()

@app.route('/categories')
def categories():
    categories = db['categories']
    categoriesReceived = categories.find()
    return render_template('Category.html', categories=categoriesReceived)

@app.route('/categories/addCategory', methods=['POST'])
def addCategory():
    categories = db['categories']
    name = request.form['name']

    if name:
        category = Category(name)
        response = jsonify({
            'name': name
        })
        categories.insert_one(category.toDBCollection())

        return redirect(url_for('categories'))
    else:
        return notFound()

@app.route('/participants')
def participants():
    participants = db['participants']
    participantsReceived = participants.find()
    return render_template('Participant.html', participants=participantsReceived)

@app.route('/participants/addParticipant', methods=['POST'])
def addParticipant():
    participants = db['participants']
    name = request.form['name']
    surname = request.form['surname']
    age = request.form['age']
    nationality = request.form['nationality']

    if name:
        participant = Participant(name, surname, age, nationality)
        response = jsonify({
            'name': name
        })
        participants.insert_one(participant.toDBCollection())

        return redirect(url_for('participants'))
    else:
        return notFound()



@app.errorhandler(404)
def notFound(error=None):
    message = {
        'message': 'No encontrado' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(debug=True, port=8082)
