from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection

from database import get_next_sequence_value as get_next_sequence_value
from models.character import Character


class CharacterCtrl:

    err_msg = 'Missing data or incorrect method';
    char_not_found_msg ='Personaje no encontrado';
    listchar_not_found_msg ='Personajes no encontrados';
    not_found = '404 Not Found';
    bad_request = '400 Bad Request';

    @staticmethod
    def render_template(db: Collection):
        characters = db['characters']
        charactersReceived = characters.find()
        return render_template('Character.html', characters=charactersReceived)

    # ---------------------------------------------------------

    @staticmethod
    def add_character(db: Collection):
        idCharacter = int(get_next_sequence_value(db, "idCharacter"))
        name = request.form.get('name')
        participant = int(request.form.get('participant'))
        age = request.form.get('age')
        if age: age = int(age)
        if name:
            character = Character(idCharacter, name, participant, age)
            db.insert_one(character.toDBCollection())

            return redirect(url_for('characters'))
        else:
            return jsonify({'error': 'Personaje no añadido', 'status': CharacterCtrl.not_found}), 404

    # ---------------------------------------------------------

    @staticmethod
    def get_character_by_name(db: Collection):
        name = request.args.get('name')
        if name:
            matchingCharacters = db.find({'name': {'$regex': name, '$options': 'i'}})
            charactersList = [
                {
                    'idCharacter': character.get('idCharacter'),
                    'name': character.get('name'),
                    'participant': character.get('participant'),
                    'age': character.get('age')
                }
                for character in matchingCharacters
            ]

            if charactersList.__len__() > 0:
                return jsonify(charactersList), 200

            else:
                return jsonify({'error': CharacterCtrl.listchar_not_found_msg, 'status': CharacterCtrl.not_found}), 404
        else:
            return jsonify({'error': 'Nombre no proporcionado', 'status': CharacterCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def get_character_by_age(db: Collection):
        age = int(request.args.get('age'))

        if age:
            matchingCharacters = db.find({'age': age})

            charactersList = [
                {
                    'idCharacter': character.get('idCharacter'),
                    'name': character.get('name'),
                    'participant': character.get('participant'),
                    'age': character.get('age')
                }
                for character in matchingCharacters
            ]

            if charactersList.__len__() > 0:
                return jsonify(charactersList), 200

            else:
                return jsonify({'error': CharacterCtrl.listchar_not_found_msg, 'status': CharacterCtrl.not_found}), 404
        else:
            return jsonify({'error': 'Edad no proporcionada', 'status': CharacterCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def get_character_by_id(db: Collection, idCharacter: int):
        if idCharacter:
            idCharacter = int(idCharacter)
            matchingCharacter = db.find({'idCharacter': idCharacter})
            charactersList = [
                {
                    'idCharacter': character.get('idCharacter'),
                    'name': character.get('name'),
                    'participant': character.get('participant'),
                    'age': character.get('age')
                }
                for character in matchingCharacter
            ]
            if charactersList.__len__()>0:
                return jsonify(charactersList)
            else:
                return jsonify({'error': CharacterCtrl.char_not_found_msg, 'status': CharacterCtrl.not_found}), 404


        else:
            return jsonify({'error': CharacterCtrl.err_msg, 'status': CharacterCtrl.bad_request}), 400

    # --------------------------------------------------------

    @staticmethod
    def get_content_by_character(characterCollection: Collection, movieCollection: Collection,
                              seriesCollection: Collection):
        idCharacter = int(request.args.get('idCharacter'))

        if idCharacter:
            contentList = []
            matchingMovie = movieCollection.find({'character': {'$in': [str(idCharacter)]}})

            contentList.append({'Content': 'Movies'})

            for movie in matchingMovie:
                contentList.append({
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
                })

            contentList.append({'Content': 'Series'})
            matchingSerie = seriesCollection.find({'character': {'$in': [str(idCharacter)]}})

            for series in matchingSerie:
                contentList.append({
                    'idSeries': series.get('idSeries'),
                    'title': series.get('title'),
                    'duration': series.get('duration'),
                    'urlTitlePage': series.get('urlTitlePage'),
                    'releaseDate': series.get('releaseDate'),
                    'synopsis': series.get('synopsis'),
                    'description': series.get('description'),
                    'isSuscription': series.get('isSuscription'),
                    'seasons': series.get('seasons'),
                    'languages': series.get('languages'),
                    'categories': series.get('categories'),
                    'characters': series.get('characters'),
                    'participants': series.get('participants'),
                    'trailer': series.get('trailer')
                })

            if contentList.__len__()>0:
                return jsonify(contentList), 200

            else:
                return jsonify({'error': CharacterCtrl.char_not_found_msg, 'status': CharacterCtrl.not_found}), 404
        else:
            return jsonify({'error': CharacterCtrl.err_msg, 'status': CharacterCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def get_all_characters(db: Collection):
        allCharacters = db.find()
        charactersList = [
            {
                'idCharacter': character.get('idCharacter'),
                'name': character.get('name'),
                'participant': character.get('participant'),
                'age': character.get('age')
            }
            for character in allCharacters
        ]
        if charactersList.__len__() > 0:
            return jsonify(charactersList), 200

        else:
            return jsonify({'error': CharacterCtrl.listchar_not_found_msg, 'status': CharacterCtrl.not_found}), 404

    # ---------------------------------------------------------

    @staticmethod
    def delete_character(db: Collection, idCharacter: int):
        if idCharacter:
            if db.delete_one({'idCharacter': idCharacter}):
                return redirect(url_for('characters'))
            else:
                return jsonify({'error': 'Character not found or not deleted', 'status': CharacterCtrl.not_found}), 404
        else:
            return jsonify({'error': CharacterCtrl.err_msg, 'status': CharacterCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def delete_character_form(db: Collection):
        idCharacter = int(request.form.get('idCharacter'))
        return CharacterCtrl.delete_character(db, idCharacter)

    @staticmethod
    def put_character(db: Collection, idCharacter: int):
        if idCharacter:
            name = request.form.get('name')
            participant = request.form.get('participant')
            age = request.form.get('age')
            if age:
                age = int(age)
            if participant:
                participant = int(participant)

            character_filter = {'idCharacter': idCharacter}

            updateFields = {}

            if name:
                updateFields['name'] = name
            if participant:
                updateFields['participant'] = participant
            if age:
                updateFields['age'] = age

            change = {'$set': updateFields}

            result = db.update_one(character_filter, change)
            if result.matched_count == 0:
                return jsonify({'error': CharacterCtrl.char_not_found_msg, 'status': CharacterCtrl.not_found}), 404
            elif result.modified_count == 0:
                return jsonify({'message': 'El personaje ya está actualizado', 'status': '200 OK'}), 200

            return redirect(url_for('characters'))

        return jsonify({'error': CharacterCtrl.err_msg, 'status': CharacterCtrl.bad_request}), 400

    @staticmethod
    def put_character_form(db: Collection):
        idCharacter = int(request.form.get('idCharacter'))
        return CharacterCtrl.put_character(db, idCharacter)

    # --------------------------------------------------------
