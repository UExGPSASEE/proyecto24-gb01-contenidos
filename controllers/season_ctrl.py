from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection

from database import get_next_sequence_value as get_next_sequence_value
from models.season import Season


class SeasonCtrl:

    err_msg = 'Missing data or incorrect method';
    not_found = '404 Not Found';

    @staticmethod
    def render_template(db: Collection):
        seasonsReceived = db.find()
        return render_template('Season.html', seasons=seasonsReceived)

    # ---------------------------------------------------------

    @staticmethod
    def addSeason(db: Collection):
        idSeason = int(get_next_sequence_value(db, "idSeason"))
        idSeries = request.form.get('idSeries')
        title = request.form.get('title')
        seasonNumber = request.form.get('seasonNumber')
        totalChapters = 0

        if idSeason:
            season = Season(idSeason, int(idSeries), title, int(seasonNumber),
                            totalChapters, None, None, None, None)

            db.insert_one(season.toDBCollection())
            return redirect(url_for('seasons'))
        else:
            return jsonify({'error': 'Temporada no añadida', 'status': SeasonCtrl.not_found}), 404

    # ---------------------------------------------------------
    @staticmethod
    def deleteSeason(db: Collection, idSeason: int):
        if idSeason:
            idSeason = int(idSeason)
            if db.delete_one({'idSeason': idSeason}):
                print("Delete ok")
                return redirect(url_for('seasons'))
            else:
                return jsonify({'error': 'Season not found or not deleted', 'status': SeasonCtrl.not_found}), 404
        else:
            return jsonify({'error': SeasonCtrl.err_msg, 'status': '400 Bad Request'}), 400

    # ---------------------------------------------------------

    @staticmethod
    def deleteSeasonForm(db: Collection):
        idSeason = int(request.form.get('idSeason'))
        return SeasonCtrl.deleteSeason(db, idSeason)

    @staticmethod
    def putSeasonForm(db: Collection):
        idSeason = int(request.form.get('idSeason'))
        return SeasonCtrl.putSeason(db, idSeason)

    @staticmethod
    def putSeason(db: Collection, idSeason: int):
        if idSeason:
            idSeries = request.form.get('idSeries')
            title = request.form.get('title')
            seasonNumber = request.form.get('seasonNumber')

            if not idSeason:
                return jsonify({'error': 'Identificador de temporada requerido', 'status': '400 Bad Request'}), 400

            filterDict = {'idSeason': idSeason}

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

            change = {'$set': updateFields}

            return SeasonCtrl.updateSeason(db, filterDict, change)

        return jsonify({'error': SeasonCtrl.err_msg, 'status': '400 Bad Request'}), 400

    # --------------------------------

    @staticmethod
    def getSeasonById(db: Collection, idSeason: int):
        if idSeason:
            idSeason = int(idSeason)
            matchingSeason = db.find({'idSeason': idSeason})
            seasonFound = [
                {
                    'idSeason': season.get('idSeason'),
                    'idSeries': season.get('idSeries'),
                    'title': season.get('title'),
                    'seasonNumber': season.get('seasonNumber'),
                    'totalChapters': season.get('totalChapters'),
                    'chapters': season.get('chapters'),
                    'characters': season.get('characters'),
                    'participants': season.get('participants'),
                    'trailer': season.get('trailer')
                }
                for season in matchingSeason
            ]
            if seasonFound.__len__()>0:
                return jsonify(seasonFound), 200
            else:
                return jsonify({'error': 'Season not found', 'status': SeasonCtrl.not_found}), 404
        return jsonify({'error': SeasonCtrl.err_msg, 'status': '400 Bad Request'}), 400

    # --------------------------------------

    @staticmethod
    def getSeasonChapters(seasonCollection: Collection, chapterCollection: Collection):
        idSeason = int(request.args.get('idSeason'))

        if idSeason:
            matchingSeason = seasonCollection.find({'idSeason': idSeason})

            if matchingSeason:
                resultList = []

                for season in matchingSeason:
                    chapterList = season.get('chapters', [])
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
                return jsonify({'error': 'Temporada no encontrada', 'status': SeasonCtrl.not_found}), 404

        else:
            return jsonify({'error':SeasonCtrl.err_msg, 'status': '400 Bad Request'}), 400

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
                return jsonify({'error': 'Temporada no encontrada', 'status': SeasonCtrl.not_found}), 404

        else:
            return jsonify({'error':SeasonCtrl.err_msg, 'status': '400 Bad Request'}), 400

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
                return jsonify({'error': 'Temporada no encontrada', 'status': SeasonCtrl.not_found}), 404

        else:
            return jsonify({'error':SeasonCtrl.err_msg, 'status': '400 Bad Request'}), 400

    @staticmethod
    def putTrailerIntoSeason(seasons: Collection, trailers: Collection, idSeason: int):
        idTrailer = request.args.get('idTrailer')
        if idTrailer:
            idTrailer = int(idTrailer)
            if trailers.find({'idTrailer': idTrailer}):
                filterDict = {'idSeason': int(idSeason)}
                change = {'$set': {'trailer': idTrailer}}
                return SeasonCtrl.updateSeason(seasons, filterDict, change)
            else:
                return jsonify({'error': 'No trailer was found', 'status': SeasonCtrl.not_found}), 400
        else:
            return jsonify({'error': SeasonCtrl.err_msg, 'status': '400 Bad Request'}), 400

    @staticmethod
    def deleteTrailerFromSeason(db: Collection, idSeason:int):
        if idSeason:
            filterDict = {'idSeason': int(idSeason)}
            change = {'$set': {'trailer': None}}
            return SeasonCtrl.updateSeason(db, filterDict, change)
        else:
            return jsonify({'error': SeasonCtrl.err_msg, 'status': '400 Bad Request'}), 400

    @staticmethod
    def putCategoryIntoSeason(seasons: Collection, categories: Collection, idSeason: int):
        idCategory = request.args.get('idCategory')
        if idCategory:
            idCategory = int(idCategory)
            if categories.find({'idCategory': idCategory}):
                filterDict = {'idSeason': int(idSeason)}
                change = {'$addToSet': {'categories': idCategory}}
                return SeasonCtrl.updateSeason(seasons, filterDict, change)
            else:
                return jsonify({'error': 'No category was found', 'status': SeasonCtrl.not_found}), 400
        else:
            return jsonify({'error': SeasonCtrl.err_msg, 'status': '400 Bad Request'}), 400

    @staticmethod
    def deleteCategoryFromSeason(seasons: Collection, idSeason: int):
        idCategory = request.args.get('idCategory')
        if idCategory:
            idCategory = int(idCategory)
            filterDict = {'idSeason': int(idSeason)}
            change = {'$pull': {'categories': idCategory}}
            return SeasonCtrl.updateSeason(seasons, filterDict, change)
        else:
            return jsonify({'error': SeasonCtrl.err_msg, 'status': '400 Bad Request'}), 400

    @staticmethod
    def putChapterIntoSeason(seasons: Collection, chapters: Collection, idSeason: int):
        idChapter = request.args.get('idChapter')
        if idChapter:
            idChapter = int(idChapter)
            if chapters.find({'idChapter': idChapter}):
                filterDict = {'idSeason': int(idSeason)}
                change = {'$addToSet': {'chapters': idChapter}}
                return SeasonCtrl.updateSeason(seasons, filterDict, change)
            else:
                return jsonify({'error': 'No chapter was found', 'status': SeasonCtrl.not_found}), 400
        else:
            return jsonify({'error': SeasonCtrl.err_msg, 'status': '400 Bad Request'}), 400

    @staticmethod
    def deleteChapterFromSeason(db: Collection, idSeason: int):
        idChapter = request.args.get('idChapter')
        if idChapter:
            idChapter = int(idChapter)
            filterDict = {'idSeason': int(idSeason)}
            change = {'$pull': {'chapters': idChapter}}
            return SeasonCtrl.updateSeason(db, filterDict, change)
        else:
            return jsonify({'error': SeasonCtrl.err_msg, 'status': '400 Bad Request'}), 400


    @staticmethod
    def updateSeason(db: Collection, filterDict: dict[str, int], changeDict: dict[str, dict]):
        result = db.update_one(filterDict, changeDict)
        print(result)
        if result.matched_count == 0:
            return jsonify({'error': 'Season not found or not updated', 'status': SeasonCtrl.not_found}), 404
        elif result.modified_count == 0:
            return jsonify({'message': 'There was no nothing to be updated or deleted', 'status': '200 OK'}), 200
        return redirect(url_for('seasons'))

    @staticmethod
    def updateSeasonSeries(db: Collection, idSeason:int, idSeries:int):
        if idSeries and idSeason:
            filterDict = {'idSeason': int(idSeason)}
            change = {'$set': {'idSeries': int(idSeries)}}
            return SeasonCtrl.updateSeasonSeries(db, filterDict, change)
        else:
            return jsonify({'error': SeasonCtrl.err_msg, 'status': '400 Bad Request'}), 400
