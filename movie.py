import database as dbase
from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection

class Movie:
    def __init__(self, name):
        self.name = name

# ---------------------------------------------------------

    def toDBCollection(self):
        return{
            'name' : self.name
        }
    
# ---------------------------------------------------------

    @staticmethod
    def template(db: Collection):
        movies_received = db.find()
        return render_template('Movie.html', movies=movies_received)


# ---------------------------------------------------------

    @staticmethod
    def addMovie(db: Collection):
        name = request.form['name']
        if name:
            movie = Movie(name)
            response = jsonify({
                'name': name
            })
            db.insert_one(movie.toDBCollection())

            return redirect(url_for('movies'))
        else:
            return jsonify({'error': 'Movie not found or not updated'}), 404

# ---------------------------------------------------------


    @staticmethod
    def delete_movie(db: Collection):
        movie_name = request.form['name']
        db.delete_one({'name': movie_name})
        if request.form.get('_method') == 'DELETE':
            movie_name = request.form['name']
            result = db.delete_one({'name': movie_name})
            if result.deleted_count == 1:
                print("Delete ok")
                return redirect(url_for('movies'))
            else:
                print("Delete failed")
                return redirect(url_for('movies'))
        else:
            return redirect(url_for('movies'))

# ---------------------------------------------------------

    @staticmethod
    def put_movie(db: Collection, movies_name):
        data = request.json

        if 'name' in data:
            result = db.update_one(data)
            if result.modified_count == 1:
                return jsonify({'message': f'Movie {movies_name} updated.'}), 200
            else:
                return jsonify({'error': 'Movie not found or not updated'}), 404
        else:
            return jsonify({'error': 'Movie not found or not updated'}), 404

# ---------------------------------------------------------

