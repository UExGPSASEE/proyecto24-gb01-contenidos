from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection

from database import get_next_sequence_value as get_next_sequence_value
from models.character import Character
from controllers.ok_ctrl import OkCtrl


class CharacterCtrl:

    err_msg = 'Missing data or incorrect method';
    char_not_found_msg ='Personaje no encontrado';
    listchar_not_found_msg ='Personajes no encontrados';
    not_found = '404 Not Found';
    bad_request = '400 Bad Request';

    @staticmethod
    def render_template(db: Collection):
        characters = db['characters']
        characters_received = characters.find()
        return render_template('Character.html', characters=characters_received)

    # ---------------------------------------------------------

    @staticmethod
    def add_character(db: Collection):
        id_character = int(get_next_sequence_value(db, "id_character"))
        name = request.form.get('name')
        participant = int(request.form.get('participant'))
        age = request.form.get('age')
        if age: age = int(age)
        if name:
            character = Character(id_character, name, participant, age)
            db.insert_one(character.to_db_collection())

            return OkCtrl.added('Character')
        else:
            return jsonify({'error': 'Personaje no añadido', 'status': CharacterCtrl.not_found}), 404

    # ---------------------------------------------------------

    @staticmethod
    def get_character_by_name(db: Collection):
        name = request.args.get('name')
        if name:
            matching_characters = db.find({'name': {'$regex': name, '$options': 'i'}})
            characters_list = [
                {
                    'id_character': character.get('id_character'),
                    'name': character.get('name'),
                    'participant': character.get('participant'),
                    'age': character.get('age')
                }
                for character in matching_characters
            ]

            if characters_list.__len__() > 0:
                return jsonify(characters_list), 200

            else:
                return jsonify({'error': CharacterCtrl.listchar_not_found_msg, 'status': CharacterCtrl.not_found}), 404
        else:
            return jsonify({'error': 'Nombre no proporcionado', 'status': CharacterCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def get_character_by_age(db: Collection):
        age = int(request.args.get('age'))

        if age:
            matching_characters = db.find({'age': age})

            characters_list = [
                {
                    'id_character': character.get('id_character'),
                    'name': character.get('name'),
                    'participant': character.get('participant'),
                    'age': character.get('age')
                }
                for character in matching_characters
            ]

            if characters_list.__len__() > 0:
                return jsonify(characters_list), 200

            else:
                return jsonify({'error': CharacterCtrl.listchar_not_found_msg, 'status': CharacterCtrl.not_found}), 404
        else:
            return jsonify({'error': 'Edad no proporcionada', 'status': CharacterCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def get_character_by_id(db: Collection, id_character: int):
        if id_character:
            id_character = int(id_character)
            matching_character = db.find({'id_character': id_character})
            characters_list = [
                {
                    'id_character': character.get('id_character'),
                    'name': character.get('name'),
                    'participant': character.get('participant'),
                    'age': character.get('age')
                }
                for character in matching_character
            ]
            if characters_list.__len__()>0:
                return jsonify(characters_list)
            else:
                return jsonify({'error': CharacterCtrl.char_not_found_msg, 'status': CharacterCtrl.not_found}), 404


        else:
            return jsonify({'error': CharacterCtrl.err_msg, 'status': CharacterCtrl.bad_request}), 400

    # --------------------------------------------------------

    @staticmethod
    def get_content_by_character(character_collection: Collection, movie_collection: Collection,
                              series_collection: Collection):
        id_character = int(request.args.get('id_character'))

        if id_character:
            content_list = []
            matching_movie = movie_collection.find({'character': {'$in': [str(id_character)]}})

            content_list.append({'Content': 'Movies'})

            for movie in matching_movie:
                content_list.append({
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
                })

            content_list.append({'Content': 'Series'})
            matching_serie = series_collection.find({'character': {'$in': [str(id_character)]}})

            for series in matching_serie:
                content_list.append({
                    'id_series': series.get('id_series'),
                    'title': series.get('title'),
                    'duration': series.get('duration'),
                    'url_title_page': series.get('url_title_page'),
                    'release_date': series.get('release_date'),
                    'synopsis': series.get('synopsis'),
                    'description': series.get('description'),
                    'is_subscription': series.get('is_subscription'),
                    'seasons': series.get('seasons'),
                    'languages': series.get('languages'),
                    'categories': series.get('categories'),
                    'characters': series.get('characters'),
                    'participants': series.get('participants'),
                    'trailer': series.get('trailer')
                })

            if content_list.__len__()>0:
                return jsonify(content_list), 200

            else:
                return jsonify({'error': CharacterCtrl.char_not_found_msg, 'status': CharacterCtrl.not_found}), 404
        else:
            return jsonify({'error': CharacterCtrl.err_msg, 'status': CharacterCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def get_all_characters(db: Collection):
        all_characters = db.find()
        characters_list = [
            {
                'id_character': character.get('id_character'),
                'name': character.get('name'),
                'participant': character.get('participant'),
                'age': character.get('age')
            }
            for character in all_characters
        ]
        if characters_list.__len__() > 0:
            return jsonify(characters_list), 200

        else:
            return jsonify({'error': CharacterCtrl.listchar_not_found_msg, 'status': CharacterCtrl.not_found}), 404

    # ---------------------------------------------------------

    @staticmethod
    def delete_character(db: Collection, id_character: int):
        if id_character:
            if db.delete_one({'id_character': id_character}):
                return OkCtrl.deleted('Character')
            else:
                return jsonify({'error': 'Character not found or not deleted', 'status': CharacterCtrl.not_found}), 404
        else:
            return jsonify({'error': CharacterCtrl.err_msg, 'status': CharacterCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def delete_character_form(db: Collection):
        id_character = int(request.form.get('id_character'))
        return CharacterCtrl.delete_character(db, id_character)

    @staticmethod
    def put_character(db: Collection, id_character: int):
        if id_character:
            name = request.form.get('name')
            participant = request.form.get('participant')
            age = request.form.get('age')
            if age:
                age = int(age)
            if participant:
                participant = int(participant)

            character_filter = {'id_character': id_character}

            update_fields = {}

            if name:
                update_fields['name'] = name
            if participant:
                update_fields['participant'] = participant
            if age:
                update_fields['age'] = age

            change = {'$set': update_fields}

            result = db.update_one(character_filter, change)
            if result.matched_count == 0:
                return jsonify({'error': CharacterCtrl.char_not_found_msg, 'status': CharacterCtrl.not_found}), 404
            elif result.modified_count == 0:
                return jsonify({'message': 'El personaje ya está actualizado', 'status': '200 OK'}), 200

            return OkCtrl.updated('Character')

        return jsonify({'error': CharacterCtrl.err_msg, 'status': CharacterCtrl.bad_request}), 400

    @staticmethod
    def put_character_form(db: Collection):
        id_character = int(request.form.get('id_character'))
        return CharacterCtrl.put_character(db, id_character)

    # --------------------------------------------------------
