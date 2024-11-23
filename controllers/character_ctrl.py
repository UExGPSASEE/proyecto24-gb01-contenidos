from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection

from database import get_next_sequence_value as get_next_sequence_value
from models.character import Character


class CharacterCtrl:

    @staticmethod
    def render_template(db: Collection):
        characters = db['characters']
        charactersReceived = characters.find()
        return render_template('Character.html', characters=charactersReceived)

    # ---------------------------------------------------------

    @staticmethod
    def addCharacter(db: Collection):
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
            return jsonify({'error': 'Personaje no añadido', 'status': '404 Not Found'}), 404

    # ---------------------------------------------------------

    @staticmethod
    def getCharacterByName(db: Collection):
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

            return jsonify(charactersList), 200
        else:
            return jsonify({'error': 'Nombre no proporcionado', 'status': '400 Bad Request'}), 400

    # ---------------------------------------------------------

    @staticmethod
    def getCharacterByAge(db: Collection):
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

            return jsonify(charactersList), 200
        else:
            return jsonify({'error': 'Edad no proporcionada', 'status': '400 Bad Request'}), 400

    # ---------------------------------------------------------

    @staticmethod
    def getCharacterById(db: Collection, idCharacter: int):
        idCharacter = request.view_args.get('idCharacter')
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
            return jsonify(charactersList), 200

        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    # --------------------------------------------------------

    @staticmethod
    def getContentByCharacter(characterCollection: Collection, movieCollection: Collection,
                              seriesCollection: Collection):
        idCharacter = int(request.args.get('idCharacter'))

        if idCharacter:
            matchingCharacter = characterCollection.find({'idCharacter': idCharacter})

            if matchingCharacter:
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
                        'language': movie.get('language'),
                        'category': movie.get('category'),
                        'character': movie.get('character'),
                        'participant': movie.get('participant'),
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
                        'language': series.get('language'),
                        'category': series.get('category'),
                        'character': series.get('character'),
                        'participant': series.get('participant'),
                        'trailer': series.get('trailer')
                    })

                return jsonify(contentList), 200

            else:
                return jsonify({'error': 'Personaje no encontrado', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Falta de datos o método incorrecto', 'status': '400 Bad Request'}), 400

    # ---------------------------------------------------------

    @staticmethod
    def getAllCharacters(db: Collection):
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
        return jsonify(charactersList), 200

    # ---------------------------------------------------------

    @staticmethod
    def deleteCharacter(db: Collection, idCharacter: int):
        if idCharacter:
            if db.delete_one({'idCharacter': idCharacter}):
                return redirect(url_for('characters'))
            else:
                return jsonify({'error': 'Character not found or not deleted', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    # ---------------------------------------------------------

    @staticmethod
    def deleteCharacterForm(db: Collection):
        idCharacter = int(request.form.get('idCharacter'))
        return CharacterCtrl.deleteCharacter(db, idCharacter)

    @staticmethod
    def putCharacter(db: Collection, idCharacter: int):
        if idCharacter:
            name = request.form.get('name')
            participant = request.form.get('participant')
            age = request.form.get('age')
            if age:
                age = int(age)
            if participant:
                participant = int(participant)

            filter = {'idCharacter': idCharacter}

            updateFields = {}

            if name:
                updateFields['name'] = name
            if participant:
                updateFields['participant'] = participant
            if age:
                updateFields['age'] = age

            change = {'$set': updateFields}

            result = db.update_one(filter, change)
            if result.matched_count == 0:
                return jsonify({'error': 'Personaje no encontrado', 'status': '404 Not Found'}), 404
            elif result.modified_count == 0:
                return jsonify({'message': 'El personaje ya está actualizado', 'status': '200 OK'}), 200

            return redirect(url_for('characters'))

        return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    @staticmethod
    def putCharacterForm(db: Collection):
        idCharacter = int(request.form.get('idCharacter'))
        return CharacterCtrl.putCharacter(db, idCharacter)

    # --------------------------------------------------------
