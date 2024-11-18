from flask import render_template, request, jsonify, redirect, url_for
from database import get_next_sequence_value as get_next_sequence_value
from pymongo.collection import Collection
from models.character import Character

class CharacterCtrl:

    @staticmethod
    def render_template(db: Collection):
        characters = db['characters']
        charactersReceived = characters.find()
        return render_template('Character.html', characters=charactersReceived)

    @staticmethod
    def addCharacter(db: Collection):
        idCharacter = get_next_sequence_value(db, "idCharacter")
        name = request.form.get('name')
        participant = int(request.form.get('participant'))
        age = request.form.get('age')
        if age: age = int(age)
        if name:
            character = Character(idCharacter, name, participant, age)
            db.insert_one(character.toDBCollection())

            return redirect(url_for('characters'))
        else:
            return jsonify({'error': 'Character not found or not added', 'status': '404 Not Found'}), 404

    # ---------------------------------------------------------

    @staticmethod
    def getCharacterByName(db: Collection):
        name = request.args.get('name')
        if name:
            matching_characters = db.find({'name': name})
            characters_list = [
                {
                    'name': character.get('name'),
                    'participant': character.get('participant'),
                    'age': character.get('age')
                }
                for character in matching_characters
            ]

            return jsonify(characters_list), 200
        else:
            return jsonify({'error': 'Nombre no proporcionado'}), 400


    @staticmethod
    def getCharacterByAge(db: Collection):
        age = int(request.args.get('age'))

        if age:
            matching_characters = db.find({'age': age})

            characters_list = [
                {
                    'name': character.get('name'),
                    'participant': character.get('participant'),
                    'age': character.get('age')
                }
                for character in matching_characters
            ]

            return jsonify(characters_list), 200
        else:
            return jsonify({'error': 'Edad no proporcionada'}), 400

    @staticmethod
    def getCharacterById(db: Collection):
        idCharacter = request.args.get('idCharacter')
        if idCharacter:
            idCharacter = int(idCharacter)
            matching_character = db.find({'idCharacter': idCharacter})
            characters_list = [
                {
                    'idCharacter': character.get('idCharacter'),
                    'name': character.get('name'),
                    'participant': character.get('participant'),
                    'age': character.get('age')
                }
                for character in matching_character
            ]
            return jsonify(characters_list), 200
        else:
            return jsonify({'error': 'idCharacter no proporcionado'}), 400


    @staticmethod
    def getAllCharacters(db: Collection):
        allCharacters = db.find()
        characters_list = [
            {
                'idCharacter': character.get('idCharacter'),
                'name': character.get('name'),
                'participant': character.get('participant'),
                'age': character.get('age')
            }
            for character in allCharacters
        ]
        return jsonify(characters_list), 200

    # ---------------------------------------------------------

    @staticmethod
    def deleteCharacter(db: Collection):
        if request.form.get('_method') == 'DELETE':
            idCharacter = int(request.form['idCharacter'])
            if idCharacter and db.delete_one({'idCharacter': idCharacter}):
                print("Delete ok")
                return redirect(url_for('characters'))
            else:
                print("Delete failed")
                return redirect(url_for('characters'))
        else:
            return redirect(url_for('characters'))

    # ---------------------------------------------------------

    @staticmethod
    def updateCharacter(db: Collection):
        if request.form.get('_method') != 'PUT':
            return jsonify({'error': 'No se puede actualizar', 'status': '400 Bad Request'}), 400
        try:
            idCharacter = int(request.form.get('idCharacter'))
            name = request.form.get('name')
            participant = request.form.get('participant')
            age = request.form.get('age')
            if age:
                age = int(age)
            if participant:
                participant = int(participant)

            filter = {'idCharacter': idCharacter}

            update_fields = {}

            if name:
                update_fields['name'] = name
            if participant:
                update_fields['participant'] = participant
            if age:
                update_fields['age'] = age

            change = {'$set': update_fields}

            result = db.update_one(filter, change)
            if result.matched_count == 0:
                return jsonify({'error': 'Personaje no encontrado', 'status': '404 Not Found'}), 404
            elif result.modified_count == 0:
                return jsonify({'message': 'El personaje ya está actualizado', 'status': '200 OK'}), 200

            return redirect(url_for('characters'))

        except ValueError:
            return jsonify({'error': 'Datos inválidos', 'status': '400 Bad Request'}), 400

        except Exception as e:
            return jsonify(
                {'error': f'Error interno del servidor: {str(e)}', 'status': '500 Internal Server Error'}
            ), 500

    # --------------------------------
