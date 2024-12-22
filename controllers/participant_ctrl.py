from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection

from database import get_next_sequence_value as get_next_sequence_value
from models.participant import Participant


class ParticipantCtrl:

    err_msg = 'Missing data or incorrect method';
    listparticipant_not_found_msg ='Participantes no encontrados';
    not_found = '404 Not Found';
    bad_request = '400 Bad Request';

    @staticmethod
    def render_template(db: Collection):
        participants = db['participants']
        participantsReceived = participants.find()
        return render_template('Participant.html', participants=participantsReceived)

    # ---------------------------------------------------------

    @staticmethod
    def add_participant(db: Collection):
        idParticipant = int(get_next_sequence_value(db, "idParticipant"))
        name = request.form.get('name')
        surname = request.form.get('surname')
        age = int(request.form.get('age'))
        nationality = request.form.get('nationality')

        if name:
            participant = Participant(idParticipant, name, surname, age, nationality)
            db.insert_one(participant.toDBCollection())

            return redirect(url_for('participants'))
        else:
            return jsonify({'error': 'Participante no añadido', 'status': ParticipantCtrl.not_found}), 404

    # ---------------------------------------------------------

    @staticmethod
    def get_participant_by_name(db: Collection):
        name = request.args.get('name')

        if name:
            matchingParticipants = db.find({'name': {'$regex': name, '$options': 'i'}})
            participantsList = [
                {
                    'idParticipant': participant.get('idParticipant'),
                    'name': participant.get('name'),
                    'surname': participant.get('surname'),
                    'age': participant.get('age'),
                    'nationality': participant.get('nationality')
                }
                for participant in matchingParticipants
            ]
            if participantsList.__len__()>0:
                return jsonify(participantsList), 200
            else:
                return jsonify({'error': ParticipantCtrl.listparticipant_not_found_msg, 'status': ParticipantCtrl.not_found}), 404

        return jsonify({'error': 'Nombre no proporcionado', 'status': ParticipantCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def get_participant_by_surname(db: Collection):
        surname = request.args.get('surname')

        if surname:
            matchingParticipants = db.find({'surname': {'$regex': surname, '$options': 'i'}})

            participantsList = [
                {
                    'idParticipant': participant.get('idParticipant'),
                    'name': participant.get('name'),
                    'surname': participant.get('surname'),
                    'age': participant.get('age'),
                    'nationality': participant.get('nationality')
                }
                for participant in matchingParticipants
            ]
            if participantsList.__len__() > 0:
                return jsonify(participantsList), 200
            else:
                return jsonify({'error': ParticipantCtrl.listparticipant_not_found_msg, 'status': ParticipantCtrl.not_found}), 404

        return jsonify({'error': 'Apellidos no proporcionados', 'status': ParticipantCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def get_participant_by_age(db: Collection):
        age = int(request.args.get('age'))

        if age:
            matching_participants = db.find({'age': age})

            participantsList = [
                {
                    'idParticipant': participant.get('idParticipant'),
                    'name': participant.get('name'),
                    'surname': participant.get('surname'),
                    'age': participant.get('age'),
                    'nationality': participant.get('nationality')
                }
                for participant in matching_participants
            ]
            if participantsList.__len__() > 0:
                return jsonify(participantsList), 200
            else:
                return jsonify({'error': ParticipantCtrl.listparticipant_not_found_msg, 'status': ParticipantCtrl.not_found}), 404

        return jsonify({'error': 'Edad no proporcionada', 'status': ParticipantCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def get_participant_by_nationality(db: Collection):
        nationality = request.args.get('nationality')
        if nationality:
            matchingParticipants = db.find({'nationality': {'$regex': nationality, '$options': 'i'}})
            participantsList = [
                {
                    'idParticipant': participant.get('idParticipant'),
                    'name': participant.get('name'),
                    'surname': participant.get('surname'),
                    'age': participant.get('age'),
                    'nationality': participant.get('nationality')
                }
                for participant in matchingParticipants
            ]
            if participantsList.__len__() > 0:
                return jsonify(participantsList), 200
            else:
                return jsonify({'error': ParticipantCtrl.listparticipant_not_found_msg, 'status': ParticipantCtrl.not_found}), 404

        else:
            return jsonify({'error': 'Nacionalidad no proporcionada', 'status': ParticipantCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def get_participant_by_id(db: Collection, idParticipant: int):
        if idParticipant:
            idParticipant = int(idParticipant)
            matchingParticipant = db.find({'idParticipant': idParticipant})

            participantsList = [
                {
                    'idParticipant': participant.get('idParticipant'),
                    'name': participant.get('name'),
                    'surname': participant.get('surname'),
                    'age': participant.get('age'),
                    'nationality': participant.get('nationality')
                }
                for participant in matchingParticipant
            ]
            if participantsList.__len__() > 0:
                return jsonify(participantsList), 200
            else:
                return jsonify({'error': ParticipantCtrl.listparticipant_not_found_msg, 'status': ParticipantCtrl.not_found}), 404

        else:
            return jsonify({'error': 'Identificador no proporcionado', 'status': ParticipantCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def get_content_by_participant(participantCollection: Collection, movieCollection: Collection,
                                seriesCollection: Collection):
        idParticipant = int(request.args.get('idParticipant'))

        if idParticipant:
            matchingParticipant = participantCollection.find({'idParticipant': idParticipant})

            if matchingParticipant:
                contentList = []
                matchingMovie = movieCollection.find({'participant': {'$in': [str(idParticipant)]}})

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
                matchingSerie = seriesCollection.find({'participant': {'$in': [str(idParticipant)]}})

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

                return jsonify(contentList), 200

            else:
                return jsonify({'error': 'Participante no encontrado', 'status': ParticipantCtrl.not_found}), 404
        else:
            return jsonify({'error':ParticipantCtrl.err_msg, 'status': ParticipantCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def get_all_participants(db: Collection):
        allParticipants = db.find()
        participants_list = [
            {
                'idParticipant': participant.get('idParticipant'),
                'name': participant.get('name'),
                'surname': participant.get('surname'),
                'age': participant.get('age'),
                'nationality': participant.get('nationality')
            }
            for participant in allParticipants
        ]
        return jsonify(participants_list), 200

    # ---------------------------------------------------------

    @staticmethod
    def delete_participant(db: Collection, idParticipant: int):

        if idParticipant:
            idParticipant = int(idParticipant)
            if db.delete_one({'idParticipant': idParticipant}):
                return redirect(url_for('participants'))
            else:
                return jsonify({'error': 'Participant not found or not deleted', 'status': ParticipantCtrl.not_found}), 404
        else:
            return jsonify({'error': ParticipantCtrl.err_msg, 'status': ParticipantCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def delete_participant_form(db: Collection):
        idParticipant = int(request.form.get('idParticipant'))
        return ParticipantCtrl.delete_participant(db, idParticipant)

    @staticmethod
    def put_participant_form(db: Collection):
        idParticipant = int(request.form.get('idParticipant'))
        return ParticipantCtrl.put_participant(db, idParticipant)

    @staticmethod
    def put_participant(db: Collection, idParticipant: int):
        if idParticipant:
            idParticipant = int(idParticipant)
            name = request.form.get('name')
            surname = request.form.get('surname')
            age = request.form.get('age')
            nationality = request.form.get('nationality')
            if age:
                age = int(age)
            if not idParticipant:
                return jsonify({'error': 'ID de participante requerido', 'status': ParticipantCtrl.bad_request}), 400

            participant_filter = {'idParticipant': idParticipant}

            updateFields = {}

            if name:
                updateFields['name'] = name
            if surname:
                updateFields['surname'] = surname
            if age:
                updateFields['age'] = age
            if nationality:
                updateFields['nationality'] = nationality

            change = {'$set': updateFields}

            result = db.update_one(participant_filter, change)
            if result.matched_count == 0:
                return jsonify({'error': 'Participante no encontrado', 'status': ParticipantCtrl.not_found}), 404
            elif result.modified_count == 0:
                return jsonify({'message': 'El participante ya está actualizado', 'status': '200 OK'}), 200

        return jsonify({'error': ParticipantCtrl.err_msg, 'status': ParticipantCtrl.bad_request}), 400

    # --------------------------------
