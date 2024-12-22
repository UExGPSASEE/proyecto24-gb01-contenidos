from datetime import datetime

from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection

from database import get_next_sequence_value as get_next_sequence_value
from models.movie import Movie
from controllers.ok_ctrl import OkCtrl


class MovieCtrl:

    err_msg = 'Missing data or incorrect method';
    movie_not_found_msg ='Película no encontrada';
    listmovies_not_found_msg = 'Películas no encontradas';
    not_found = '404 Not Found';
    bad_request = '400 Bad Request';

    @staticmethod
    def render_template(db: Collection):
        movies_received = db.find()
        return render_template('Movie.html', movies=movies_received)

    # ---------------------------------------------------------

    @staticmethod
    def add_movie(db: Collection):
        id_movie = int(get_next_sequence_value(db, "id_movie"))
        movie_title = request.form.get('title')
        duration = request.form.get('duration')
        url_video = request.form.get('url_video')
        url_title_page = request.form.get('url_title_page')
        release_date = request.form.get('release_date')
        synopsis = request.form.get('synopsis')
        description = request.form.get('description')
        is_subscription = request.form.get('is_subscription')

        if id_movie:
            movie = Movie(id_movie, movie_title, url_video, url_title_page, release_date, synopsis, description,
                          is_subscription, duration, None, None, None, None, None)
            db.insert_one(movie.to_db_collection())
            return OkCtrl.added('Movie')
        else:
            return jsonify({'error': 'Película no añadida', 'status': MovieCtrl.not_found}), 404

    # ---------------------------------------------------------

    @staticmethod
    def get_movie_by_id(db: Collection, id_movie: int):
        if id_movie:
            id_movie = int(id_movie)
            matching_movie = db.find({'id_movie': id_movie})

            movieFound = [
                {
                    'id_movie': movie.get('id_movie'),
                    'title': movie.get('title'),
                    'url_video': movie.get('url_video'),
                    'url_title_page': movie.get('url_title_page'),
                    'release_date': movie.get('release_date'),
                    'synopsis': movie.get('synopsis'),
                    'description': movie.get('description'),
                    'is_subscription': movie.get('is_subscription'),
                    'duration': movie.get('duration'),
                    'languages': movie.get('languages'),
                    'categories': movie.get('categories'),
                    'characters': movie.get('characters'),
                    'participants': movie.get('participants'),
                    'trailer': movie.get('trailer'),
                }
                for movie in matching_movie
            ]
            if movieFound.__len__()>0:
                return jsonify(movieFound), 200

            else:
                return jsonify({'error': MovieCtrl.movie_not_found_msg, 'status': MovieCtrl.not_found}), 404

        else:
            return jsonify({'error': MovieCtrl.err_msg, 'status': MovieCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def get_movie_characters(movie_collection: Collection, character_collection: Collection):
        id_movie = int(request.args.get('id_movie'))

        if id_movie:
            matching_movie = movie_collection.find({'id_movie': id_movie})

            characters_list = []

            for movie in matching_movie:
                characterIds = movie.get('character', [])

                for id_character in characterIds:
                    if id_character and id_character.strip().isdigit():
                        matching_character = character_collection.find({'id_character': int(id_character)})

                        for character in matching_character:
                            characters_list.append({
                                'id_character': character.get('id_character'),
                                'name': character.get('name'),
                                'participant': character.get('participant'),
                                'age': character.get('age')
                            })

                    else:
                        print(f"id_character inválido encontrado: {id_character}")

            if characters_list.__len__()>0:
                return jsonify(characters_list), 200

            else:
                return jsonify({'error': 'Personajes no encontrados', 'status': MovieCtrl.not_found}), 404

        else:
            return jsonify({'error': MovieCtrl.err_msg, 'status': MovieCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def get_movie_participants(movie_collection, participants_collection):
        id_movie = int(request.args.get('id_movie'))

        if id_movie:
            matching_movie = movie_collection.find({'id_movie': id_movie})

            participants_list = []

            for movie in matching_movie:
                participants_ids = movie.get('participant', [])

                for id_participant in participants_ids:

                    if id_participant and id_participant.strip().isdigit():
                        matching_participant = participants_collection.find({'id_participant': int(id_participant)})

                        for participant in matching_participant:
                            participants_list.append({
                                'name': participant.get('name'),
                                'surname': participant.get('surname'),
                                'age': participant.get('age'),
                                'nationality': participant.get('nationality')
                            })

                    else:
                        print(f"id_participant inválido encontrado: {id_participant}")
            if participants_list.__len__()>0:
                return jsonify(participants_list), 200
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
                        'id_movie': movie.get('id_movie'),
                        'title': movie.get('title'),
                        'url_video': movie.get('url_video'),
                        'url_title_page': movie.get('url_title_page'),
                        'release_date': movie.get('release_date'),
                        'synopsis': movie.get('synopsis'),
                        'description': movie.get('description'),
                        'is_subscription': movie.get('is_subscription'),
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
                    return jsonify({'error': MovieCtrl.movie_not_found_msg, 'status': MovieCtrl.not_found}), 404

            else:
                return jsonify({'error': MovieCtrl.listmovies_not_found_msg, 'status': MovieCtrl.not_found}), 404

        else:
            return jsonify({'error': MovieCtrl.err_msg, 'status': MovieCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def get_movie_by_release_date(db: Collection):
        release_date_str = request.args.get('release_date')

        if release_date_str:
            release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
            matching_movies = db.find({'release_date': str(release_date)})

            if db.count_documents({'release_date': str(release_date)}) > 0:
                movieFound = [
                    {
                        'id_movie': movie.get('id_movie'),
                        'title': movie.get('title'),
                        'url_video': movie.get('url_video'),
                        'url_title_page': movie.get('url_title_page'),
                        'release_date': movie.get('release_date'),
                        'synopsis': movie.get('synopsis'),
                        'description': movie.get('description'),
                        'is_subscription': movie.get('is_subscription'),
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
                    return jsonify({'error': MovieCtrl.listmovies_not_found_msg, 'status': MovieCtrl.not_found}), 404

            else:
                return jsonify({'error': MovieCtrl.listmovies_not_found_msg, 'status': MovieCtrl.not_found}), 404

        else:
            return jsonify({'error': MovieCtrl.err_msg, 'status': MovieCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def get_all_movies(db: Collection):
        all_movies = db.find()

        if db.count_documents({}) > 0:
            movies_list = [
                {
                    'id_movie': movie.get('id_movie'),
                    'title': movie.get('title'),
                    'url_video': movie.get('url_video'),
                    'url_title_page': movie.get('url_title_page'),
                    'release_date': movie.get('release_date'),
                    'synopsis': movie.get('synopsis'),
                    'description': movie.get('description'),
                    'is_subscription': movie.get('is_subscription'),
                    'duration': movie.get('duration'),
                    'languages': movie.get('languages'),
                    'categories': movie.get('categories'),
                    'characters': movie.get('characters'),
                    'participants': movie.get('participants'),
                    'trailer': movie.get('trailer'),
                }
                for movie in all_movies
            ]
            if movies_list.__len__()>0:
               return jsonify(movies_list), 200
        return jsonify({'error': MovieCtrl.listmovies_not_found_msg, 'status': MovieCtrl.not_found}), 404

    # ---------------------------------------------------------

    @staticmethod
    def delete_movie(db: Collection, id_movie: int):
        if id_movie:
            id_movie = int(id_movie)
            if db.delete_one({'id_movie': id_movie}):
                return OkCtrl.deleted('Movie')
            else:
                return jsonify({'error': 'Movie not found or not deleted', 'status': MovieCtrl.not_found}), 404
        else:
            return jsonify({'error': MovieCtrl.err_msg, 'status': MovieCtrl.bad_request}), 400

    @staticmethod
    def delete_movie_form(db: Collection):
        id_movie = int(request.form.get('id_movie'))
        return MovieCtrl.delete_movie(db, id_movie)
    # ---------------------------------------------------------

    @staticmethod
    def put_movie(db: Collection, id_movie: int):
        if id_movie:
            id_movie = int(id_movie)
            movie_title = request.form.get('title')
            duration = request.form.get('duration')
            url_video = request.form.get('url_video')
            url_title_page = request.form.get('url_title_page')
            release_date = request.form.get('release_date')
            synopsis = request.form.get('synopsis')
            description = request.form.get('description')
            is_subscription = request.form.get('is_subscription')

            filter_dict = {'id_movie': id_movie}

            update_fields = {}

            if movie_title:
                update_fields['title'] = movie_title
            if duration:
                update_fields['duration'] = int(duration)
            if url_video:
                update_fields['url_video'] = url_video
            if url_title_page:
                update_fields['url_title_page'] = url_title_page
            if release_date:
                update_fields['release_date'] = release_date
            if synopsis:
                update_fields['synopsis'] = synopsis
            if description:
                update_fields['description'] = description
            if is_subscription:
                update_fields['is_subscription'] = is_subscription

            change = {'$set': update_fields}
            return MovieCtrl.update_movie(db, filter_dict, change)

        return jsonify({'error': MovieCtrl.err_msg, 'status': MovieCtrl.bad_request}), 400

    @staticmethod
    def put_movie_form(db: Collection):
        id_movie = int(request.form.get('id_movie'))
        return MovieCtrl.put_movie(db, id_movie)

# --------------------------------

    @staticmethod
    def put_trailer_into_movie(movies: Collection, trailers: Collection, id_movie: int):
        id_trailer = request.args.get('id_trailer')
        if id_trailer:
            id_trailer = int(id_trailer)
            if trailers.find({'id_trailer': id_trailer}):
                filter_dict = {'id_movie': int(id_movie)}
                change = {'$set': {'trailer': id_trailer}}
                return MovieCtrl.update_movie(movies, filter_dict, change)
            else:
                return jsonify({'error': 'No trailer was found', 'status': MovieCtrl.not_found}), 400
        else:
            return jsonify({'error': MovieCtrl.err_msg, 'status': MovieCtrl.bad_request}), 400

    @staticmethod
    def delete_trailer_from_movie(db: Collection, id_movie:int):
        if id_movie:
            filter_dict = {'id_movie': int(id_movie)}
            change = {'$set': {'trailer': None}}
            return MovieCtrl.update_movie(db, filter_dict, change)
        else:
            return jsonify({'error': MovieCtrl.err_msg, 'status': MovieCtrl.bad_request}), 400

    @staticmethod
    def put_category_into_movie(movies: Collection, categories: Collection, id_movie: int):
        id_category = request.args.get('id_category')
        if id_category:
            id_category = int(id_category)
            if categories.find({'id_category': id_category}):
                filter_dict = {'id_movie': int(id_movie)}
                change = {'$addToSet': {'categories': id_category}}
                return MovieCtrl.update_movie(movies, filter_dict, change)
            else:
                return jsonify({'error': 'No category was found', 'status': MovieCtrl.not_found}), 400
        else:
            return jsonify({'error': MovieCtrl.err_msg, 'status': MovieCtrl.bad_request}), 400

    @staticmethod
    def delete_category_from_movie(movies: Collection, id_movie: int):
        id_category = request.args.get('id_category')
        if id_category:
            id_category = int(id_category)
            filter_dict = {'id_movie': int(id_movie)}
            change = {'$pull': {'categories': id_category}}
            return MovieCtrl.update_movie(movies, filter_dict, change)
        else:
            return jsonify({'error': MovieCtrl.err_msg, 'status': MovieCtrl.bad_request}), 400

    @staticmethod
    def update_movie(db: Collection, filter_dict: dict[str, int], change_dict: dict[str, dict]):
        result = db.update_one(filter_dict, change_dict)
        print(result)
        if result.matched_count == 0:
            return jsonify({'error': 'Movie not found or not updated', 'status': MovieCtrl.not_found}), 404
        elif result.modified_count == 0:
            return jsonify({'message': 'There was no nothing to be updated or deleted', 'status': '200 OK'}), 200
        return OkCtrl.updated('Movie')
