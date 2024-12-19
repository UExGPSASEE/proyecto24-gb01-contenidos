from datetime import datetime

from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection

from database import get_next_sequence_value as get_next_sequence_value
from models.movie import Movie


class MovieCtrl:

    err_msg = 'Missing data or incorrect method';
    not_found = '404 Not Found';
    bad_request = '400 Bad Request';

    @staticmethod
    def render_template(db: Collection):
        moviesReceived = db.find()
        return render_template('Movie.html', movies=moviesReceived)

    # ---------------------------------------------------------

    @staticmethod
    def add_movie(db: Collection):
        idMovie = int(get_next_sequence_value(db, "idMovie"))
        movieTitle = request.form.get('title')
        duration = request.form.get('duration')
        urlVideo = request.form.get('urlVideo')
        urlTitlePage = request.form.get('urlTitlePage')
        releaseDate = request.form.get('releaseDate')
        synopsis = request.form.get('synopsis')
        description = request.form.get('description')
        isSuscription = request.form.get('isSuscription')

        if idMovie:
            movie = Movie(idMovie, movieTitle, urlVideo, urlTitlePage, releaseDate, synopsis, description,
                          isSuscription, duration, None, None, None, None, None)
            db.insert_one(movie.toDBCollection())
            return redirect(url_for('movies'))
        else:
            return jsonify({'error': 'Película no añadida', 'status': MovieCtrl.not_found}), 404

    # ---------------------------------------------------------

    @staticmethod
    def get_movie_by_id(db: Collection, idMovie: int):
        if idMovie:
            idMovie = int(idMovie)
            matchingMovie = db.find({'idMovie': idMovie})

            movieFound = [
                {
                    'idMovie': movie.get('idMovie'),
                    'title': movie.get('title'),
                    'urlVideo': movie.get('urlVideo'),
                    'urlTitlePage': movie.get('urlTitlePage'),
                    'releaseDate': movie.get('releaseDate'),
                    'synopsis': movie.get('synopsis'),
                    'description': movie.get('description'),
                    'isSuscription': movie.get('isSuscription'),
                    'duration': movie.get('duration'),
                    'languages': movie.get('languages'),
                    'categories': movie.get('categories'),
                    'characters': movie.get('characters'),
                    'participants': movie.get('participants'),
                    'trailer': movie.get('trailer'),
                }
                for movie in matchingMovie
            ]
            if movieFound.__len__()>0:
                return jsonify(movieFound), 200

            else:
                return jsonify({'error': 'Película no encontrada', 'status': MovieCtrl.not_found}), 404

        else:
            return jsonify({'error': MovieCtrl.err_msg, 'status': MovieCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def get_movie_characters(movieCollection: Collection, characterCollection: Collection):
        idMovie = int(request.args.get('idMovie'))

        if idMovie:
            matchingMovie = movieCollection.find({'idMovie': idMovie})

            charactersList = []

            for movie in matchingMovie:
                characterIds = movie.get('character', [])

                for idCharacter in characterIds:
                    if idCharacter and idCharacter.strip().isdigit():
                        matchingCharacter = characterCollection.find({'idCharacter': int(idCharacter)})

                        for character in matchingCharacter:
                            charactersList.append({
                                'idCharacter': character.get('idCharacter'),
                                'name': character.get('name'),
                                'participant': character.get('participant'),
                                'age': character.get('age')
                            })

                    else:
                        print(f"idCharacter inválido encontrado: {idCharacter}")

            if charactersList.__len__()>0:
                return jsonify(charactersList), 200

            else:
                return jsonify({'error': 'Personajes no encontrados', 'status': MovieCtrl.not_found}), 404

        else:
            return jsonify({'error': MovieCtrl.err_msg, 'status': MovieCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def get_movie_participants(movieCollection, participantsCollection):
        idMovie = int(request.args.get('idMovie'))

        if idMovie:
            matchingMovie = movieCollection.find({'idMovie': idMovie})

            participantsList = []

            for movie in matchingMovie:
                participantsIds = movie.get('participant', [])

                for idParticipant in participantsIds:

                    if idParticipant and idParticipant.strip().isdigit():
                        matchingParticipant = participantsCollection.find({'idParticipant': int(idParticipant)})

                        for participant in matchingParticipant:
                            participantsList.append({
                                'name': participant.get('name'),
                                'surname': participant.get('surname'),
                                'age': participant.get('age'),
                                'nationality': participant.get('nationality')
                            })

                    else:
                        print(f"idParticipant inválido encontrado: {idParticipant}")
            if participantsList.__len__()>0:
                return jsonify(participantsList), 200
            else:
                return jsonify({'error': 'Participantes no encontrados', 'status': MovieCtrl.not_found}), 404
        else:
            return jsonify({'error': MovieCtrl.err_msg, 'status': MovieCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def get_movie_by_title(db: Collection):
        title = request.args.get('title')

        if title:
            matching_movie = db.find({'title': {'$regex': title, '$options': 'i'}})

            if db.count_documents({'title': {'$regex': title, '$options': 'i'}}) > 0:
                movieFound = [
                    {
                        'idMovie': movie.get('idMovie'),
                        'title': movie.get('title'),
                        'urlVideo': movie.get('urlVideo'),
                        'urlTitlePage': movie.get('urlTitlePage'),
                        'releaseDate': movie.get('releaseDate'),
                        'synopsis': movie.get('synopsis'),
                        'description': movie.get('description'),
                        'isSuscription': movie.get('isSuscription'),
                        'duration': movie.get('duration'),
                        'languages': movie.get('languages'),
                        'categories': movie.get('categories'),
                        'characters': movie.get('characters'),
                        'participants': movie.get('participants'),
                        'trailer': movie.get('trailer'),
                    }
                    for movie in matching_movie
                ]
                if movieFound.__len__() > 0:
                    return jsonify(movieFound), 200
                else:
                    return jsonify({'error': 'Película no encontrada', 'status': MovieCtrl.not_found}), 404

            else:
                return jsonify({'error': 'No se han encontrado películas', 'status': MovieCtrl.not_found}), 404

        else:
            return jsonify({'error': MovieCtrl.err_msg, 'status': MovieCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def get_movie_by_release_date(db: Collection):
        releaseDate_str = request.args.get('releaseDate')

        if releaseDate_str:
            releaseDate = datetime.strptime(releaseDate_str, '%Y-%m-%d').date()
            matching_movies = db.find({'releaseDate': str(releaseDate)})

            if db.count_documents({'releaseDate': str(releaseDate)}) > 0:
                movieFound = [
                    {
                        'idMovie': movie.get('idMovie'),
                        'title': movie.get('title'),
                        'urlVideo': movie.get('urlVideo'),
                        'urlTitlePage': movie.get('urlTitlePage'),
                        'releaseDate': movie.get('releaseDate'),
                        'synopsis': movie.get('synopsis'),
                        'description': movie.get('description'),
                        'isSuscription': movie.get('isSuscription'),
                        'duration': movie.get('duration'),
                        'languages': movie.get('languages'),
                        'categories': movie.get('categories'),
                        'characters': movie.get('characters'),
                        'participants': movie.get('participants'),
                        'trailer': movie.get('trailer'),
                    }
                    for movie in matching_movies
                ]
                if movieFound.__len__() > 0:
                    return jsonify(movieFound), 200
                else:
                    return jsonify({'error': 'Película no encontrada', 'status': MovieCtrl.not_found}), 404

            else:
                return jsonify({'error': 'Película no encontrada', 'status': MovieCtrl.not_found}), 404

        else:
            return jsonify({'error': MovieCtrl.err_msg, 'status': MovieCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def get_all_movies(db: Collection):
        allMovies = db.find()

        if db.count_documents({}) > 0:
            movies_list = [
                {
                    'idMovie': movie.get('idMovie'),
                    'title': movie.get('title'),
                    'urlVideo': movie.get('urlVideo'),
                    'urlTitlePage': movie.get('urlTitlePage'),
                    'releaseDate': movie.get('releaseDate'),
                    'synopsis': movie.get('synopsis'),
                    'description': movie.get('description'),
                    'isSuscription': movie.get('isSuscription'),
                    'duration': movie.get('duration'),
                    'languages': movie.get('languages'),
                    'categories': movie.get('categories'),
                    'characters': movie.get('characters'),
                    'participants': movie.get('participants'),
                    'trailer': movie.get('trailer'),
                }
                for movie in allMovies
            ]
            if movies_list.__len__()>0:
               return jsonify(movies_list), 200
        return jsonify({'error': 'No existen películas insertadas', 'status': MovieCtrl.not_found}), 404

    # ---------------------------------------------------------

    @staticmethod
    def delete_movie(db: Collection, idMovie: int):
        if idMovie:
            idMovie = int(idMovie)
            if db.delete_one({'idMovie': idMovie}):
                return redirect(url_for('movies'))
            else:
                return jsonify({'error': 'Movie not found or not deleted', 'status': MovieCtrl.not_found}), 404
        else:
            return jsonify({'error': MovieCtrl.err_msg, 'status': MovieCtrl.bad_request}), 400

    @staticmethod
    def delete_movie_form(db: Collection):
        idMovie = int(request.form.get('idMovie'))
        return MovieCtrl.delete_movie(db, idMovie)
    # ---------------------------------------------------------

    @staticmethod
    def put_movie(db: Collection, idMovie: int):
        if idMovie:
            idMovie = int(idMovie)
            movieTitle = request.form.get('title')
            duration = request.form.get('duration')
            urlVideo = request.form.get('urlVideo')
            urlTitlePage = request.form.get('urlTitlePage')
            releaseDate = request.form.get('releaseDate')
            synopsis = request.form.get('synopsis')
            description = request.form.get('description')
            isSuscription = request.form.get('isSuscription')

            filterDict = {'idMovie': idMovie}

            updateFields = {}

            if movieTitle:
                updateFields['title'] = movieTitle
            if duration:
                updateFields['duration'] = int(duration)
            if urlVideo:
                updateFields['urlVideo'] = urlVideo
            if urlTitlePage:
                updateFields['urlTitlePage'] = urlTitlePage
            if releaseDate:
                updateFields['releaseDate'] = releaseDate
            if synopsis:
                updateFields['synopsis'] = synopsis
            if description:
                updateFields['description'] = description
            if isSuscription:
                updateFields['isSuscription'] = isSuscription

            change = {'$set': updateFields}
            return MovieCtrl.update_movie(db, filterDict, change)

        return jsonify({'error': MovieCtrl.err_msg, 'status': MovieCtrl.bad_request}), 400

    @staticmethod
    def put_movie_form(db: Collection):
        idMovie = int(request.form.get('idMovie'))
        return MovieCtrl.put_movie(db, idMovie)

# --------------------------------

    @staticmethod
    def put_trailer_into_movie(movies: Collection, trailers: Collection, idMovie: int):
        idTrailer = request.args.get('idTrailer')
        if idTrailer:
            idTrailer = int(idTrailer)
            if trailers.find({'idTrailer': idTrailer}):
                filterDict = {'idMovie': int(idMovie)}
                change = {'$set': {'trailer': idTrailer}}
                return MovieCtrl.update_movie(movies, filterDict, change)
            else:
                return jsonify({'error': 'No trailer was found', 'status': MovieCtrl.not_found}), 400
        else:
            return jsonify({'error': MovieCtrl.err_msg, 'status': MovieCtrl.bad_request}), 400

    @staticmethod
    def delete_trailer_from_movie(db: Collection, idMovie:int):
        if idMovie:
            filterDict = {'idMovie': int(idMovie)}
            change = {'$set': {'trailer': None}}
            return MovieCtrl.update_movie(db, filterDict, change)
        else:
            return jsonify({'error': MovieCtrl.err_msg, 'status': MovieCtrl.bad_request}), 400

    @staticmethod
    def put_category_into_movie(movies: Collection, categories: Collection, idMovie: int):
        idCategory = request.args.get('idCategory')
        if idCategory:
            idCategory = int(idCategory)
            if categories.find({'idCategory': idCategory}):
                filterDict = {'idMovie': int(idMovie)}
                change = {'$addToSet': {'categories': idCategory}}
                return MovieCtrl.update_movie(movies, filterDict, change)
            else:
                return jsonify({'error': 'No category was found', 'status': MovieCtrl.not_found}), 400
        else:
            return jsonify({'error': MovieCtrl.err_msg, 'status': MovieCtrl.bad_request}), 400

    @staticmethod
    def delete_category_from_movie(movies: Collection, idMovie: int):
        idCategory = request.args.get('idCategory')
        if idCategory:
            idCategory = int(idCategory)
            filterDict = {'idMovie': int(idMovie)}
            change = {'$pull': {'categories': idCategory}}
            return MovieCtrl.update_movie(movies, filterDict, change)
        else:
            return jsonify({'error': MovieCtrl.err_msg, 'status': MovieCtrl.bad_request}), 400

    @staticmethod
    def update_movie(db: Collection, filterDict: dict[str, int], changeDict: dict[str, dict]):
        result = db.update_one(filterDict, changeDict)
        print(result)
        if result.matched_count == 0:
            return jsonify({'error': 'Movie not found or not updated', 'status': MovieCtrl.not_found}), 404
        elif result.modified_count == 0:
            return jsonify({'message': 'There was no nothing to be updated or deleted', 'status': '200 OK'}), 200
        return redirect(url_for('movies'))
