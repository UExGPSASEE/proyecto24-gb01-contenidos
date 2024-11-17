from flask import render_template, request, jsonify, redirect, url_for
from database import get_next_sequence_value as get_next_sequence_value
from datetime import datetime
from pymongo.collection import Collection
from models.movie import Movie

class MovieCtrl:
    @staticmethod
    def render_template(db: Collection):
        moviesReceived = db.find()
        return render_template('Movie.html', movies=moviesReceived)

# ---------------------------------------------------------

    @staticmethod
    def addMovie(db: Collection):
        idMovie = get_next_sequence_value(db,"idMovie")
        movie_title = request.form.get('title')
        duration = request.form.get('duration')
        urlVideo = request.form.get('urlVideo')
        urlTitlePage = request.form.get('urlTitlePage')
        releaseDate = request.form.get('releaseDate')
        synopsis = request.form.get('synopsis')
        description = request.form.get('description')
        language = request.form.getlist('language[]')
        category = request.form.getlist('category[]')
        character = request.form.getlist('character[]')
        participant = request.form.getlist('participant[]')
        trailer = request.form.get('trailer')
        if idMovie:
            movie = Movie(idMovie, movie_title, urlVideo, urlTitlePage, releaseDate, synopsis, description,
                          None, duration, language, category, character, participant, trailer)
            db.insert_one(movie.toDBCollection())
            return redirect(url_for('movies'))
        else:
            return jsonify({'error': 'Movie not found or not added', 'status':'404 Not Found'}), 404

# ---------------------------------------------------------

    @staticmethod
    def getMovieById(db: Collection):
        idMovie = int(request.args.get('idMovie'))
        if idMovie:
            matching_movie = db.find({'idMovie': idMovie})
            if matching_movie:
                movieFound = [
                {
                    'idMovie' : movie.get('idMovie'),
                    'title' : movie.get('title'),
                    'urlVideo' : movie.get('urlVideo'),
                    'urlTitlePage' : movie.get('urlTitlePage'),
                    'releaseDate' : movie.get('releaseDate'),
                    'synopsis' : movie.get('synopsis'),
                    'description' : movie.get('description'),
                    'isSuscription' : movie.get('isSuscription'),
                    'duration' : movie.get('duration'),
                    'language' : movie.get('language'),
                    'category' : movie.get('category'),
                    'character' : movie.get('character'),
                    'participant' : movie.get('participant'),
                    'trailer' : movie.get('trailer'),
                }
                for movie in matching_movie
                ]
                return jsonify(movieFound), 200
            else:
                return jsonify({'error': 'Movie not found', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

# ---------------------------------------------------------

    @staticmethod
    def getMovieByTitle(db: Collection):
        title = request.args.get('title')
        if title:
            matching_movie = db.find({'title': title})
            if matching_movie:
                movieFound = [
                {
                    'idMovie' : movie.get('idMovie'),
                    'title' : movie.get('title'),
                    'urlVideo' : movie.get('urlVideo'),
                    'urlTitlePage' : movie.get('urlTitlePage'),
                    'releaseDate' : movie.get('releaseDate'),
                    'synopsis' : movie.get('synopsis'),
                    'description' : movie.get('description'),
                    'isSuscription' : movie.get('isSuscription'),
                    'duration' : movie.get('duration'),
                    'language' : movie.get('language'),
                    'category' : movie.get('category'),
                    'character' : movie.get('character'),
                    'participant' : movie.get('participant'),
                    'trailer' : movie.get('trailer'),
                }
                for movie in matching_movie
                ]
                return jsonify(movieFound), 200
            else:
                return jsonify({'error': 'Movie not found', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

# ---------------------------------------------------------

    @staticmethod
    def getMovieByReleaseDate(db: Collection):
        releaseDate_str = request.args.get('releaseDate')
        if releaseDate_str:
            releaseDate = datetime.strptime(releaseDate_str, '%Y-%m-%d').date()
            # Busca películas que coincidan con el releaseDate
            matching_movies = db.find({'releaseDate': str(releaseDate)})  # Asegúrate de que el formato coincida con el almacenado en la DB
            if matching_movies:
                movieFound = [
                {
                    'idMovie' : movie.get('idMovie'),
                    'title' : movie.get('title'),
                    'urlVideo' : movie.get('urlVideo'),
                    'urlTitlePage' : movie.get('urlTitlePage'),
                    'releaseDate' : movie.get('releaseDate'),
                    'synopsis' : movie.get('synopsis'),
                    'description' : movie.get('description'),
                    'isSuscription' : movie.get('isSuscription'),
                    'duration' : movie.get('duration'),
                    'language' : movie.get('language'),
                    'category' : movie.get('category'),
                    'character' : movie.get('character'),
                    'participant' : movie.get('participant'),
                    'trailer' : movie.get('trailer'),
                }
                for movie in matching_movies
                ]
                return jsonify(movieFound), 200
            else:
                return jsonify({'error': 'Movie not found', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

# ---------------------------------------------------------

    @staticmethod
    def getAllMovies(db: Collection):
        allMovies = db.find()
        movies_list = [
            {
                'idMovie' : movie.get('idMovie'),
                'title' : movie.get('title'),
                'urlVideo' : movie.get('urlVideo'),
                'urlTitlePage' : movie.get('urlTitlePage'),
                'releaseDate' : movie.get('releaseDate'),
                'synopsis' : movie.get('synopsis'),
                'description' : movie.get('description'),
                'isSuscription' : movie.get('isSuscription'),
                'duration' : movie.get('duration'),
                'language' : movie.get('language'),
                'category' : movie.get('category'),
                'character' : movie.get('character'),
                'participant' : movie.get('participant'),
                'trailer' : movie.get('trailer'),
            }
            for movie in allMovies
        ]
        return jsonify(movies_list), 200

# ---------------------------------------------------------

    @staticmethod
    def delete_movie(db: Collection):
        if request.form.get('_method') == 'DELETE':
            movie_id = int(request.form['id'])
            if movie_id and db.delete_one({'idMovie': movie_id}):
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
        if request.form.get('_method') != 'PUT':
            return jsonify({'error': 'No se puede actualizar', 'status': '400 Bad Request'}), 400
        try:
            movie_id = int(request.form.get('id'))
            movie_title = request.form.get('title')
            duration = request.form.get('duration')
            urlVideo = request.form.get('urlVideo')
            urlTitlePage = request.form.get('urlTitlePage')
            releaseDate = request.form.get('releaseDate')
            synopsis = request.form.get('synopsis')
            description = request.form.get('description')
            language = request.form.getlist('language[]')
            category = request.form.getlist('category[]')
            character = request.form.getlist('character[]')
            participant = request.form.getlist('participant[]')
            trailer = request.form.get('trailer')

            if not movie_id:
                return jsonify({'error': 'ID de película requerido', 'status': '400 Bad Request'}), 400

            filter = {'idMovie': movie_id}

            update_fields = {}

            if movie_title:
                update_fields['title'] = movie_title
            if duration:
                update_fields['duration'] = int(duration)  # Convertir a entero si aplica
            if urlVideo:
                update_fields['urlVideo'] = urlVideo
            if urlTitlePage:
                update_fields['urlTitlePage'] = urlTitlePage
            if releaseDate:
                update_fields['releaseDate'] = releaseDate
            if synopsis:
                update_fields['synopsis'] = synopsis
            if description:
                update_fields['description'] = description
            if language:
                update_fields['language'] = language
            if category:
                update_fields['category'] = category
            if character:
                update_fields['character'] = character
            if participant:
                update_fields['participant'] = participant
            if trailer:
                update_fields['trailer'] = trailer

            change = {'$set': update_fields}

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
            return jsonify(
                {'error': f'Error interno del servidor: {str(e)}', 'status': '500 Internal Server Error'}
            ), 500

# --------------------------------
