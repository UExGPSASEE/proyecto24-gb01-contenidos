from flask import render_template, request, jsonify, redirect, url_for
from database import get_next_sequence_value as get_next_sequence_value
from pymongo.collection import Collection
from models.series import Series

class SeriesCtrl:
    @staticmethod
    def render_template(db: Collection):
        seriesReceived = db.find()
        return render_template('Series.html', series=seriesReceived)

# --------------------------------------------------------------

    @staticmethod
    def addSeries(db: Collection):
        idSeries = get_next_sequence_value(db,"idSeries")
        title = request.form.get('title')
        duration = request.form.get('duration')
        urlTitlePage = request.form.get('urlTitlePage')
        releaseDate = request.form.get('releaseDate')
        synopsis = request.form.get('synopsis')
        description = request.form.get('description')
        language = request.form.getlist('language[]')
        category = request.form.getlist('category[]')
        character = request.form.getlist('character[]')
        participant = request.form.getlist('participant[]')
        seasons = request.form.getlist('seasons[]')
        trailer = request.form.get('trailer')
        isSuscription = request.form.get('isSuscription')

        if idSeries:
            series = Series(idSeries, title, seasons, urlTitlePage, releaseDate, synopsis, description,
                          isSuscription, duration, language, category, character, participant, trailer)
            db.insert_one(series.toDBCollection())
            return redirect(url_for('series'))
        else:
            return jsonify({'error': 'Serie no añadida', 'status':'404 Not Found'}), 404

# --------------------------------------------------------------

    @staticmethod
    def getSeriesByTitle(db: Collection):
        title = request.args.get('title')

        if title:
            matching_series = db.find({'title': {'$regex': title, '$options': 'i'}})

            if db.count_documents({'title': {'$regex': title, '$options': 'i'}}) > 0:
                seriesFound = [
                {
                    'idSeries' : series.get('idSeries'),
                    'title' : series.get('title'),
                    'duration' : series.get('duration'),
                    'urlTitlePage' : series.get('urlTitlePage'),
                    'releaseDate' : series.get('releaseDate'),
                    'synopsis' : series.get('synopsis'),
                    'description' : series.get('description'),
                    'isSuscription' : series.get('isSuscription'), # OJO
                    'seasons': series.get('seasons'),
                    'language' : series.get('language'),
                    'category' : series.get('category'),
                    'character' : series.get('character'),
                    'participant' : series.get('participant'),
                    'trailer' : series.get('trailer')
                }
                for series in matching_series
                ]
                return jsonify(seriesFound), 200

            else:
                return jsonify({'error': 'No se han encontrado series', 'status': '404 Not Found'}), 404

        else:
            return jsonify({'error': 'Falta de datos o método incorrecto', 'status': '400 Bad Request'}), 400

# --------------------------------------------------------------

    @staticmethod
    def getSeriesById(db: Collection):
        idSeries = int(request.args.get('idSeries'))

        if idSeries:
            matching_series = db.find({'idSeries': idSeries})

            if matching_series:
                seriesFound = [
                {
                    'idSeries' : series.get('idSeries'),
                    'title' : series.get('title'),
                    'duration' : series.get('duration'),
                    'urlTitlePage' : series.get('urlTitlePage'),
                    'releaseDate' : series.get('releaseDate'),
                    'synopsis' : series.get('synopsis'),
                    'description' : series.get('description'),
                    'isSuscription' : series.get('isSuscription'),
                    'seasons': series.get('seasons'),
                    'language' : series.get('language'),
                    'category' : series.get('category'),
                    'character' : series.get('character'),
                    'participant' : series.get('participant'),
                    'trailer' : series.get('trailer')
                }
                for series in matching_series
                ]
                return jsonify(seriesFound), 200

            else:
                return jsonify({'error': 'Serie no encontrada', 'status': '404 Not Found'}), 404

        else:
            return jsonify({'error': 'Falta de datos o método incorrecto', 'status': '400 Bad Request'}), 400

# --------------------------------------------------------------

    @staticmethod
    def getSeriesCharacters(seriesCollection: Collection, characterCollection: Collection):
        idSeries = int(request.args.get('idSeries'))

        if idSeries:
            matchingSeries = seriesCollection.find({'idSeries': idSeries})

            if matchingSeries:
                charactersList = []

                for series in matchingSeries:
                    characterIds = series.get('character', [])

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
                return jsonify({'error': 'Serie no encontrada', 'status': '404 Not Found'}), 404

        else:
            return jsonify({'error': 'Falta de datos o método incorrecto', 'status': '400 Bad Request'}), 400

# --------------------------------------------------------------

    @staticmethod
    def getSeriesParticipants(seriesCollection, participantsCollection):
        idSeries = int(request.args.get('idSeries'))

        if idSeries:
            matchingSeries = seriesCollection.find({'idSeries': idSeries})

            if matchingSeries:
                participantsList = []

                for series in matchingSeries:
                    participantsIds = series.get('participant', [])

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
                return jsonify(participantsList), 200

            else:
                return jsonify({'error': 'Serie no encontrada', 'status': '404 Not Found'}), 404

        else:
            return jsonify({'error': 'Falta de datos o método incorrecto', 'status': '400 Bad Request'}), 400

# --------------------------------------------------------------

    @staticmethod
    def getAllSeries(db: Collection):
        allSeries = db.find()

        if db.count_documents({}) > 0:
            series_list = [
                {
                    'idSeries' : series.get('idSeries'),
                    'title' : series.get('title'),
                    'duration' : series.get('duration'),
                    'urlTitlePage' : series.get('urlTitlePage'),
                    'releaseDate' : series.get('releaseDate'),
                    'synopsis' : series.get('synopsis'),
                    'description' : series.get('description'),
                    'isSuscription' : series.get('isSuscription'),
                    'seasons': series.get('seasons'),
                    'language' : series.get('language'),
                    'category' : series.get('category'),
                    'character' : series.get('character'),
                    'participant' : series.get('participant'),
                    'trailer' : series.get('trailer')
                }
                for series in allSeries
            ]
            return jsonify(series_list), 200

        else:
            return jsonify({'error': 'No existen películas insertadas', 'status': '404 Not Found'}), 404

# --------------------------------------------------------------

    @staticmethod
    def delete_series(db: Collection):
        if request.form.get('_method') == 'DELETE':
            idSeries = int(request.form['idSeries'])
            if idSeries and db.delete_one({'idSeries': idSeries}):
                print("Delete ok")
                return redirect(url_for('series'))
            else:
                print("Delete failed")
                return redirect(url_for('series'))
        else:
            return redirect(url_for('series'))

# --------------------------------------------------------------

    @staticmethod
    def put_series(db: Collection):
        if request.form.get('_method') != 'PUT':
            return jsonify({'error': 'No se puede actualizar', 'status': '400 Bad Request'}), 400
        try:
            idSeries = int(request.form.get('idSeries'))
            title = request.form.get('title')
            duration = request.form.get('duration')
            seasons = request.form.get('seasons[]')
            urlTitlePage = request.form.get('urlTitlePage')
            releaseDate = request.form.get('releaseDate')
            synopsis = request.form.get('synopsis')
            description = request.form.get('description')
            language = request.form.getlist('language[]')
            category = request.form.getlist('category[]')
            character = request.form.getlist('character[]')
            participant = request.form.getlist('participant[]')
            trailer = request.form.get('trailer')
            isSuscription = request.form.get('isSuscription')

            if not idSeries:
                return jsonify({'error': 'Identificador de serie requerido', 'status': '400 Bad Request'}), 400

            filter = {'idSeries': idSeries}

            updateFields = {}

            if title:
                updateFields['title'] = title
            if duration:
                updateFields['duration'] = int(duration)
            if seasons:
                updateFields['seasons'] = seasons
            if urlTitlePage:
                updateFields['urlTitlePage'] = urlTitlePage
            if releaseDate:
                updateFields['releaseDate'] = releaseDate
            if synopsis:
                updateFields['synopsis'] = synopsis
            if description:
                updateFields['description'] = description
            if language:
                updateFields['language'] = language
            if category:
                updateFields['category'] = category
            if character:
                updateFields['character'] = character
            if participant:
                updateFields['participant'] = participant
            if trailer:
                updateFields['trailer'] = trailer
            if isSuscription:
                updateFields['isSuscription'] = isSuscription

            change = {'$set': updateFields}

            result = db.update_one(filter, change)
            if result.matched_count == 0:
                return jsonify({'error': 'Serie no encontrada', 'status': '404 Not Found'}), 404
            elif result.modified_count == 0:
                return jsonify({'message': 'La serie ya está actualizada', 'status': '200 OK'}), 200

            return redirect(url_for('series'))

        except ValueError:
            return jsonify({'error': 'Datos inválidos', 'status': '400 Bad Request'}), 400

        except Exception as e:
            return jsonify(
                {'error': f'Error interno del servidor: {str(e)}', 'status': '500 Internal Server Error'}
            ), 500
