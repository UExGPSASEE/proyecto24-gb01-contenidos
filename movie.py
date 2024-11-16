import database as dbase
from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection
from database import get_next_id

class Movie:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

# ---------------------------------------------------------

    def toDBCollection(self, id):
        return{
            'name' : self.name,
            'duration' : self.duration,
            'id': id
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
        duration = request.form['duration']
        if name:
            movie_id = get_next_id('movies')
            movie = Movie(name, duration)
            db.insert_one(movie.toDBCollection(movie_id))
            return redirect(url_for('movies'))
        else:
            return jsonify({'error': 'Movie not found or not updated'}), 404

# ---------------------------------------------------------


    @staticmethod
    def delete_movie(db: Collection):
        if request.form.get('_method') == 'DELETE':
            movie_id = int(request.form['id'])

            if movie_id and db.delete_one({'id': movie_id}):
                print("Delete ok")
                return redirect(url_for('movies'))
            else:
                print("Delete failed")
                return redirect(url_for('movies'))
        else:
            return redirect(url_for('movies'))

# ---------------------------------------------------------

    @staticmethod
    def put_movie(db: Collection):
        try:
            # Validar datos del formulario
            movie_id = int(request.form.get('id'))
            movie_name = request.form.get('name')
            duration = int(request.form.get('duration'))

            if not (movie_id and movie_name and duration):
                    return jsonify({'error': 'Datos incompletos', 'status': '400 Bad Request'}), 400

            filter = {'id': movie_id}
            if movie_name and duration:
                change = {'$set': {'name': movie_name,
                                   'duration': duration}}
            elif movie_name: change = {'$set': {'name': movie_name}}
            elif duration: change = {'$set': {'duration': duration}}

            else: change = {}

            result = db.update_one(filter, change)

            if result.matched_count == 0:
                return jsonify({'error': 'Película no encontrada', 'status': '404 Not Found'}), 404
            elif result.modified_count == 0:
                return jsonify({'message': 'La película ya está actualizada', 'status': '200 OK'}), 200
            # Redirigir a la lista de películas
            return redirect(url_for('movies'))

        except ValueError:
             return jsonify({'error': 'Datos inválidos', 'status': '400 Bad Request'}), 400

        except Exception as e:
            return jsonify({'error': f'Error interno del servidor: {str(e)}', 'status': '500 Internal Server Error'}), 500

# ---------------------------------------------------------

