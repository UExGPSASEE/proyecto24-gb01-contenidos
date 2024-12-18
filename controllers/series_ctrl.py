from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection

from database import get_next_sequence_value as get_next_sequence_value
from models.series import Series
from controllers.season_ctrl import SeasonCtrl


class SeriesCtrl:

    err_msg = 'Missing data or incorrect method';
    not_found = '404 Not Found';

    @staticmethod
    def render_template(db: Collection):
        seriesReceived = db.find()
        return render_template('Series.html', series=seriesReceived)

    # --------------------------------------------------------------

    @staticmethod
    def addSeries(db: Collection):
        idSeries = int(get_next_sequence_value(db, "idSeries"))
        title = request.form.get('title')
        duration = request.form.get('duration')
        urlTitlePage = request.form.get('urlTitlePage')
        releaseDate = request.form.get('releaseDate')
        synopsis = request.form.get('synopsis')
        description = request.form.get('description')
        isSuscription = request.form.get('isSuscription')

        if idSeries:
            series = Series(idSeries, title, None, urlTitlePage, releaseDate, synopsis, description,
                            isSuscription, duration, None, None, None, None, None)
            db.insert_one(series.toDBCollection())
            return redirect(url_for('series'))
        else:
            return jsonify({'error': 'Serie no añadida', 'status': SeriesCtrl.not_found}), 404

    # --------------------------------------------------------------

    @staticmethod
    def getSeriesByTitle(db: Collection):
        title = request.args.get('title')

        if title:
            matching_series = db.find({'title': {'$regex': title, '$options': 'i'}})

            if db.count_documents({'title': {'$regex': title, '$options': 'i'}}) > 0:
                seriesFound = [
                    {
                        'idSeries': series.get('idSeries'),
                        'title': series.get('title'),
                        'duration': series.get('duration'),
                        'urlTitlePage': series.get('urlTitlePage'),
                        'releaseDate': series.get('releaseDate'),
                        'synopsis': series.get('synopsis'),
                        'description': series.get('description'),
                        'isSuscription': series.get('isSuscription'),  # OJO
                        'seasons': series.get('seasons'),
                        'languages': series.get('languages'),
                        'categories': series.get('categories'),
                        'characters': series.get('characters'),
                        'participants': series.get('participants'),
                        'trailer': series.get('trailer')
                    }
                    for series in matching_series
                ]
                return jsonify(seriesFound), 200

            else:
                return jsonify({'error': 'No se han encontrado series', 'status': SeriesCtrl.not_found}), 404

        else:
            return jsonify({'error': SeriesCtrl.err_msg, 'status': '400 Bad Request'}), 400

    # --------------------------------------------------------------

    @staticmethod
    def getSeriesById(db: Collection, idSeries: int):
        if idSeries:
            idSeries = int(idSeries)
            matching_series = db.find({'idSeries': idSeries})
            seriesFound = [
                {
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
                }
                for series in matching_series
            ]
            if seriesFound.__len__()>0:
                return jsonify(seriesFound), 200
            else:
                return jsonify({'error': 'Serie no encontrada', 'status': SeriesCtrl.not_found}), 404

        else:
            return jsonify({'error': SeriesCtrl.err_msg, 'status': '400 Bad Request'}), 400

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
                return jsonify({'error': 'Serie no encontrada', 'status': SeriesCtrl.not_found}), 404

        else:
            return jsonify({'error': SeriesCtrl.err_msg, 'status': '400 Bad Request'}), 400

    # --------------------------------------------------------------

    @staticmethod
    def getSeriesChapters(seriesCollection: Collection, seasonCollection: Collection):
        idSeries = int(request.args.get('idSeries'))
        print(idSeries)

        if idSeries:
            matchingSeries = seriesCollection.find({'idSeries': idSeries})

            if matchingSeries:
                seasonsList = []

                for series in matchingSeries:
                    seasonsIds = series.get('seasons', [])
                    print(seasonsIds)

                    for idSeason in seasonsIds:

                        if idSeason and idSeason.strip().isdigit():
                            matchingSeason = seasonCollection.find(
                                {'idSeason': int(idSeason), 'idSeries': int(idSeries)})

                            for season in matchingSeason:
                                seasonsList.append({
                                    'idSeason': season.get('idSeason'),
                                    'idSeries': season.get('idSeries'),
                                    'title': season.get('title'),
                                    'seasonNumber': season.get('seasonNumber'),
                                    'totalChapters': season.get('totalChapters'),
                                    'chapters': season.get('chapters'),
                                    'characters': season.get('characters'),
                                    'participants': season.get('participants'),
                                    'trailer': season.get('trailer')
                                })

                return jsonify(seasonsList), 200

            else:
                return jsonify({'error': 'Serie no encontrada', 'status': SeriesCtrl.not_found}), 404

        else:
            return jsonify({'error': SeriesCtrl.err_msg, 'status': '400 Bad Request'}), 400

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
                return jsonify({'error': 'Serie no encontrada', 'status': SeriesCtrl.not_found}), 404

        else:
            return jsonify({'error': SeriesCtrl.err_msg, 'status': '400 Bad Request'}), 400

    # --------------------------------------------------------------

    @staticmethod
    def getAllSeries(db: Collection):
        allSeries = db.find()

        if db.count_documents({}) > 0:
            series_list = [
                {
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
                }
                for series in allSeries
            ]
            return jsonify(series_list), 200

        else:
            return jsonify({'error': 'No existen películas insertadas', 'status': SeriesCtrl.not_found}), 404

    # --------------------------------------------------------------

    @staticmethod
    def deleteSeries(db: Collection, idSeries: int):
        if idSeries:
            idSeries = int(idSeries)
            if db.delete_one({'idSeries': idSeries}):
                return redirect(url_for('series'))
            else:
                return jsonify({'error': 'Series not found or not deleted', 'status': SeriesCtrl.not_found}), 404
        else:
            return jsonify({'error': SeriesCtrl.err_msg, 'status': '400 Bad Request'}), 400

    # --------------------------------------------------------------

    @staticmethod
    def deleteSeriesForm(db: Collection):
        idSeries = int(request.form.get('idSeries'))
        return SeriesCtrl.deleteSeries(db, idSeries)

    @staticmethod
    def putSeriesForm(db: Collection):
        idSeries = int(request.form.get('idSeries'))
        return SeriesCtrl.putSeries(db, idSeries)

    @staticmethod
    def putSeries(db: Collection, idSeries: int):
        if idSeries:
            idSeries = int(idSeries)
            title = request.form.get('title')
            duration = request.form.get('duration')
            seasons = request.form.get('seasons[]')
            urlTitlePage = request.form.get('urlTitlePage')
            releaseDate = request.form.get('releaseDate')
            synopsis = request.form.get('synopsis')
            description = request.form.get('description')
            isSuscription = request.form.get('isSuscription')

            if not idSeries:
                return jsonify({'error': 'Identificador de serie requerido', 'status': '400 Bad Request'}), 400

            filterDict = {'idSeries': idSeries}

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
            if isSuscription:
                updateFields['isSuscription'] = isSuscription

            change = {'$set': updateFields}

            return SeriesCtrl.updateSeries(db, filterDict, change)

        return jsonify({'error': SeriesCtrl.err_msg, 'status': '400 Bad Request'}), 400

    @staticmethod
    def putTrailerIntoSeries(series: Collection, trailers: Collection, idSeries: int):
        idTrailer = request.args.get('idTrailer')
        if idTrailer:
            idTrailer = int(idTrailer)
            if trailers.find({'idTrailer': idTrailer}):
                filterDict = {'idSeries': int(idSeries)}
                change = {'$set': {'trailer': idTrailer}}
                return SeriesCtrl.updateSeries(series, filterDict, change)
            else:
                return jsonify({'error': 'No trailer was found', 'status': SeriesCtrl.not_found}), 400
        else:
            return jsonify({'error': SeriesCtrl.err_msg, 'status': '400 Bad Request'}), 400

    @staticmethod
    def deleteTrailerFromSeries(db: Collection, idSeries:int):
        if idSeries:
            filterDict = {'idSeries': int(idSeries)}
            change = {'$set': {'trailer': None}}
            return SeriesCtrl.updateSeries(db, filterDict, change)
        else:
            return jsonify({'error': SeriesCtrl.err_msg, 'status': '400 Bad Request'}), 400

    @staticmethod
    def putCategoryIntoSeries(series: Collection, categories: Collection, idSeries: int):
        idCategory = request.args.get('idCategory')
        if idCategory:
            idCategory = int(idCategory)
            if categories.find({'idCategory': idCategory}):
                filterDict = {'idSeries': int(idSeries)}
                change = {'$addToSet': {'categories': idCategory}}
                return SeriesCtrl.updateSeries(series, filterDict, change)
            else:
                return jsonify({'error': 'No category was found', 'status': SeriesCtrl.not_found}), 400
        else:
            return jsonify({'error': SeriesCtrl.err_msg, 'status': '400 Bad Request'}), 400

    @staticmethod
    def deleteCategoryFromSeries(series: Collection, idSeries: int):
        idCategory = request.args.get('idCategory')
        if idCategory:
            idCategory = int(idCategory)
            filterDict = {'idSeries': int(idSeries)}
            change = {'$pull': {'categories': idCategory}}
            return SeriesCtrl.updateSeries(series, filterDict, change)
        else:
            return jsonify({'error': SeriesCtrl.err_msg, 'status': '400 Bad Request'}), 400

    @staticmethod
    def putSeasonIntoSeries(series: Collection, seasons: Collection, idSeries: int):
        idSeason = request.args.get('idSeason')
        if idSeason:
            idSeason = int(idSeason)
            if seasons.find({'idSeason': idSeason}):
                filterDict = {'idSeries': int(idSeries)}
                change = {'$addToSet': {'seasons': idSeason}}
                SeasonCtrl.updateSeasonSeries(seasons, idSeason, idSeries)
                return SeriesCtrl.updateSeries(series, filterDict, change)
            else:
                return jsonify({'error': 'No season was found', 'status': SeriesCtrl.not_found}), 400
        else:
            return jsonify({'error': SeriesCtrl.err_msg, 'status': '400 Bad Request'}), 400

    @staticmethod
    def deleteSeasonFromSeries(series: Collection, idSeries: int):
        idSeason = request.args.get('idSeason')
        if idSeason:
            idSeason = int(idSeason)
            filterDict = {'idSeries': int(idSeries)}
            change = {'$pull': {'seasons': idSeason}}
            return SeriesCtrl.updateSeries(series, filterDict, change)
        else:
            return jsonify({'error': SeriesCtrl.err_msg, 'status': '400 Bad Request'}), 400

    @staticmethod
    def updateSeries(db: Collection, filterDict: dict[str, int], changeDict: dict[str, dict]):
        result = db.update_one(filterDict, changeDict)
        print(result)
        if result.matched_count == 0:
            return jsonify({'error': 'Series not found or not updated', 'status': SeriesCtrl.not_found}), 404
        elif result.modified_count == 0:
            return jsonify({'message': 'There was no nothing to be updated or deleted', 'status': '200 OK'}), 200
        return redirect(url_for('series'))

