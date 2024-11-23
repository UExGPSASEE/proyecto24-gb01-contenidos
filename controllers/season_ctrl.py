from flask import render_template, request, jsonify, redirect, url_for
from database import get_next_sequence_value as get_next_sequence_value
from pymongo.collection import Collection
from models.season import Season
from controllers.character_ctrl import CharacterCtrl

class SeasonCtrl:
    @staticmethod
    def render_template(db: Collection):
        seasonsReceived = db.find()
        return render_template('Season.html', seasons=seasonsReceived)

# ---------------------------------------------------------

    @staticmethod
    def addSeason(db: Collection):
        idSeason = get_next_sequence_value(db,"idSeason")
        idSeries = request.form.get('idSeries')
        title = request.form.get('title')
        seasonNumber = request.form.get('seasonNumber')
        chapterList = request.form.getlist('chapterList[]')
        character = request.form.getlist('character[]')
        participant = request.form.getlist('participant[]')
        trailer = request.form.get('trailer')

        totalChapters = len([chapter for chapter in chapterList if chapter != ""])

        if idSeason:
            season = Season(idSeason, int(idSeries), title, int(seasonNumber),
                            totalChapters, chapterList, character, participant, trailer)

            db.insert_one(season.toDBCollection())
            return redirect(url_for('seasons'))
        else:
            return jsonify({'error': 'Temporada no añadida', 'status':'404 Not Found'}), 404

# ---------------------------------------------------------
    @staticmethod
    def delete_season(db: Collection):
        if request.form.get('_method') == 'DELETE':
            idSeason = int(request.form['idSeason'])
            if idSeason and db.delete_one({'idSeason': idSeason}):
                print("Delete ok")
                return redirect(url_for('seasons'))
            else:
                print("Delete failed")
                return redirect(url_for('seasons'))
        else:
            return redirect(url_for('seasons'))

# ---------------------------------------------------------

    @staticmethod
    def put_season(db: Collection):
        if request.form.get('_method') != 'PUT':
            return jsonify({'error': 'No se puede actualizar', 'status': '400 Bad Request'}), 400
        try:
            idSeason = int(request.form.get('idSeason'))
            idSeries = request.form.get('idSeries')
            title = request.form.get('title')
            seasonNumber = request.form.get('seasonNumber')
            chapterList = request.form.getlist('chapterList[]')
            character = request.form.getlist('character[]')
            participant = request.form.getlist('participant[]')
            trailer = request.form.get('trailer')

            if not idSeason:
                return jsonify({'error': 'Identificador de temporada requerido', 'status': '400 Bad Request'}), 400

            filter = {'idSeason': idSeason}

            totalChapters = len([chapter for chapter in chapterList if chapter != ""])

            updateFields = {}

            if idSeries:
                updateFields['idSeries'] = int(idSeries)
            if title:
                updateFields['title'] = title
            if seasonNumber:
                updateFields['seasonNumber'] = int(seasonNumber)
            if totalChapters:
                updateFields['totalChapters'] = int(totalChapters)
            if chapterList:
                updateFields['chapterList'] = chapterList
            if character:
                updateFields['character'] = character
            if participant:
                updateFields['participant'] = participant
            if trailer:
                updateFields['trailer'] = trailer

            change = {'$set': updateFields}

            result = db.update_one(filter, change)
            if result.matched_count == 0:
                return jsonify({'error': 'Temporada no encontrada', 'status': '404 Not Found'}), 404
            elif result.modified_count == 0:
                return jsonify({'message': 'La temporada ya está actualizada', 'status': '200 OK'}), 200

            return redirect(url_for('seasons'))

        except ValueError:
            return jsonify({'error': 'Datos inválidos', 'status': '400 Bad Request'}), 400

        except Exception as e:
            return jsonify(
                {'error': f'Error interno del servidor: {str(e)}', 'status': '500 Internal Server Error'}
            ), 500

# --------------------------------

    @staticmethod
    def getSeasonById(db: Collection):
        idSeason = int(request.args.get('idSeason'))
        if idSeason:
            matchingSeason = db.find({'idSeason': idSeason})
            if matchingSeason:
                seasonFound = [
                {
                    'idSeason' : season.get('idSeason'),
                    'idSeries' : season.get('idSeries'),
                    'title' : season.get('title'),
                    'seasonNumber' : season.get('seasonNumber'),
                    'totalChapters' : season.get('totalChapters'),
                    'chapterList' : season.get('chapterList'),
                    'character' : season.get('character'),
                    'participant' : season.get('participant'),
                    'trailer' : season.get('trailer')
                }
                for season in matchingSeason
                ]
                return jsonify(seasonFound), 200
            else:
                return jsonify({'error': 'Season not found', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

# --------------------------------------

    @staticmethod
    def getSeasonChapters(seasonCollection: Collection, chapterCollection: Collection):
        idSeason = int(request.args.get('idSeason'))

        if idSeason:
            matchingSeason = seasonCollection.find({'idSeason': idSeason})

            if matchingSeason:
                resultList = []

                for season in matchingSeason:
                    chapterList = season.get('chapterList', [])
                    print(chapterList)

                    for idChapter in chapterList:
                        if isinstance(idChapter, (str, int)):
                            idChapterStr = str(idChapter).strip()
                            if idChapterStr.isdigit():
                                matchingCharacter = chapterCollection.find({'idChapter': int(idChapterStr)})

                                for character in matchingCharacter:
                                    resultList.append({
                                        'idChapter': character.get('idChapter'),
                                        'title': character.get('title'),
                                        'urlVideo': character.get('urlVideo'),
                                        'duration': character.get('duration'),
                                        'chapterNumber': character.get('chapterNumber')
                                    })
                            else:
                                print(f"idChapter inválido encontrado: {idChapter}")
                        else:
                            print(f"idChapter no es del tipo esperado: {idChapter}")

                return jsonify(resultList), 200

            else:
                return jsonify({'error': 'Temporada no encontrada', 'status': '404 Not Found'}), 404

        else:
            return jsonify({'error': 'Falta de datos o método incorrecto', 'status': '400 Bad Request'}), 400

# --------------------------------------

    @staticmethod
    def getSeasonCharacters(seasonCollection: Collection, characterCollection: Collection):
        idSeason = int(request.args.get('idSeason'))

        if idSeason:
            matchingSeason = seasonCollection.find({'idSeason': idSeason})

            if matchingSeason:
                charactersList = []

                for season in matchingSeason:
                    characterIds = season.get('character', [])

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

                return jsonify(charactersList), 200

            else:
                return jsonify({'error': 'Temporada no encontrada', 'status': '404 Not Found'}), 404

        else:
            return jsonify({'error': 'Falta de datos o método incorrecto', 'status': '400 Bad Request'}), 400

# --------------------------------------

    @staticmethod
    def getSeasonParticipants(seasonCollection: Collection, participantCollection: Collection):
        idSeason = int(request.args.get('idSeason'))

        if idSeason:
            matchingSeason = seasonCollection.find({'idSeason': idSeason})

            if matchingSeason:
                participantsList = []

                for season in matchingSeason:
                    participantIds = season.get('participant', [])

                    for idParticipant in participantIds:

                        if idParticipant and idParticipant.strip().isdigit():
                            matchingParticipant = participantCollection.find({'idParticipant': int(idParticipant)})

                            for participant in matchingParticipant:
                                participantsList.append({
                                    'idParticipant': participant.get('idParticipant'),
                                    'name': participant.get('name'),
                                    'surname': participant.get('surname'),
                                    'age': participant.get('age')
                                })

                        else:
                            print(f"idParticipant inválido encontrado: {idParticipant}")

                return jsonify(participantsList), 200

            else:
                return jsonify({'error': 'Temporada no encontrada', 'status': '404 Not Found'}), 404

        else:
            return jsonify({'error': 'Falta de datos o método incorrecto', 'status': '400 Bad Request'}), 400
