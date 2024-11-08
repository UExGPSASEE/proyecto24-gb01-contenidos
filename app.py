import database as dbase
from flask import Flask, render_template, request, jsonify, redirect, url_for
from movie import Movie

db = dbase.conexionMongoDB()

app = Flask(__name__)


@app.route('/')
def home():
    movies = db['Movies']
    moviesReceived = movies.find()
    return render_template('index.html', movies=moviesReceived)


@app.route('/movies', methods=['POST'])
def addMovie():
    movies = db['Movies']
    name = request.form['name']

    if name:
        movie = Movie(name)
        response = jsonify({
            'name': name
        })
        movies.insert_one(movie.toDBCollection())

        return redirect(url_for('home'))
    else:
        return notFound()


@app.route('/movies/delete/<string:movies_name>', methods=['DELETE'])
def deleteMovie(movie_name):
    movies = db['Movies']
    movies.delete_one({'name': movie_name})
    return redirect(url_for('home'))


@app.route('/movies/put/<string:movies_name>', methods=['PUT'])
def putMovie(movie_name):
    movies = db['Movies']
    name = request.form['name']

    if name:
        movies.update_one({'name': movie_name}, {'$set': {'name': name}})
        response = jsonify({'message': 'Movie' + movie_name + 'updated.'})
        return redirect(url_for('home'))
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
    app.run(debug=True, port=8080)