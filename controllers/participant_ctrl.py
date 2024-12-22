from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection

from database import get_next_sequence_value as get_next_sequence_value
from models.participant import Participant
from controllers.ok_ctrl import OkCtrl


class ParticipantCtrl:

    err_msg = 'Missing data or incorrect method';
    listparticipant_not_found_msg ='Participantes no encontrados';
    not_found = '404 Not Found';
    bad_request = '400 Bad Request';

    @staticmethod
    def render_template(db: Collection):
        participants = db['participants']
        participants_received = participants.find()
        return render_template('Participant.html', participants=participants_received)

    # ---------------------------------------------------------

    @staticmethod
    def add_participant(db: Collection):
        id_participant = int(get_next_sequence_value(db, "id_participant"))
        name = request.form.get('name')
        surname = request.form.get('surname')
        age = int(request.form.get('age'))
        nationality = request.form.get('nationality')

        if name:
            participant = Participant(id_participant, name, surname, age, nationality)
            db.insert_one(participant.to_db_collection())

            return OkCtrl.added('Participant')
        else:
            return jsonify({'error': 'Participante no añadido', 'status': ParticipantCtrl.not_found}), 404

    # ---------------------------------------------------------

    @staticmethod
    def get_participant_by_name(db: Collection):
        name = request.args.get('name')

        if name:
            matching_participants = db.find({'name': {'$regex': name, '$options': 'i'}})
            participants_list = [
                {
                    'id_participant': participant.get('id_participant'),
                    'name': participant.get('name'),
                    'surname': participant.get('surname'),
                    'age': participant.get('age'),
                    'nationality': participant.get('nationality')
                }
                for participant in matching_participants
            ]
            if participants_list.__len__()>0:
                return jsonify(participants_list), 200
            else:
                return jsonify({'error': ParticipantCtrl.listparticipant_not_found_msg, 'status': ParticipantCtrl.not_found}), 404

        return jsonify({'error': 'Nombre no proporcionado', 'status': ParticipantCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def get_participant_by_surname(db: Collection):
        surname = request.args.get('surname')

        if surname:
            matching_participants = db.find({'surname': {'$regex': surname, '$options': 'i'}})

            participants_list = [
                {
                    'id_participant': participant.get('id_participant'),
                    'name': participant.get('name'),
                    'surname': participant.get('surname'),
                    'age': participant.get('age'),
                    'nationality': participant.get('nationality')
                }
                for participant in matching_participants
            ]
            if participants_list.__len__() > 0:
                return jsonify(participants_list), 200
            else:
                return jsonify({'error': ParticipantCtrl.listparticipant_not_found_msg, 'status': ParticipantCtrl.not_found}), 404

        return jsonify({'error': 'Apellidos no proporcionados', 'status': ParticipantCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def get_participant_by_age(db: Collection):
        age = int(request.args.get('age'))

        if age:
            matching_participants = db.find({'age': age})

            participants_list = [
                {
                    'id_participant': participant.get('id_participant'),
                    'name': participant.get('name'),
                    'surname': participant.get('surname'),
                    'age': participant.get('age'),
                    'nationality': participant.get('nationality')
                }
                for participant in matching_participants
            ]
            if participants_list.__len__() > 0:
                return jsonify(participants_list), 200
            else:
                return jsonify({'error': ParticipantCtrl.listparticipant_not_found_msg, 'status': ParticipantCtrl.not_found}), 404

        return jsonify({'error': 'Edad no proporcionada', 'status': ParticipantCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def get_participant_by_nationality(db: Collection):
        nationality = request.args.get('nationality')
        if nationality:
            matching_participants = db.find({'nationality': {'$regex': nationality, '$options': 'i'}})
            participants_list = [
                {
                    'id_participant': participant.get('id_participant'),
                    'name': participant.get('name'),
                    'surname': participant.get('surname'),
                    'age': participant.get('age'),
                    'nationality': participant.get('nationality')
                }
                for participant in matching_participants
            ]
            if participants_list.__len__() > 0:
                return jsonify(participants_list), 200
            else:
                return jsonify({'error': ParticipantCtrl.listparticipant_not_found_msg, 'status': ParticipantCtrl.not_found}), 404

        else:
            return jsonify({'error': 'Nacionalidad no proporcionada', 'status': ParticipantCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def get_participant_by_id(db: Collection, id_participant: int):
        if id_participant:
            id_participant = int(id_participant)
            matching_participant = db.find({'id_participant': id_participant})

            participants_list = [
                {
                    'id_participant': participant.get('id_participant'),
                    'name': participant.get('name'),
                    'surname': participant.get('surname'),
                    'age': participant.get('age'),
                    'nationality': participant.get('nationality')
                }
                for participant in matching_participant
            ]
            if participants_list.__len__() > 0:
                return jsonify(participants_list), 200
            else:
                return jsonify({'error': ParticipantCtrl.listparticipant_not_found_msg, 'status': ParticipantCtrl.not_found}), 404

        else:
            return jsonify({'error': 'Identificador no proporcionado', 'status': ParticipantCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def get_content_by_participant(participant_collection: Collection, movie_collection: Collection,
                                series_collection: Collection):
        id_participant = int(request.args.get('id_participant'))

        if id_participant:
            matching_participant = participant_collection.find({'id_participant': id_participant})

            if matching_participant:
                content_list = []
                matching_movie = movie_collection.find({'participant': {'$in': [str(id_participant)]}})

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
                matching_serie = series_collection.find({'participant': {'$in': [str(id_participant)]}})

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

                return jsonify(content_list), 200

            else:
                return jsonify({'error': 'Participante no encontrado', 'status': ParticipantCtrl.not_found}), 404
        else:
            return jsonify({'error':ParticipantCtrl.err_msg, 'status': ParticipantCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def get_all_participants(db: Collection):
        all_participants = db.find()
        participants_list = [
            {
                'id_participant': participant.get('id_participant'),
                'name': participant.get('name'),
                'surname': participant.get('surname'),
                'age': participant.get('age'),
                'nationality': participant.get('nationality')
            }
            for participant in all_participants
        ]
        return jsonify(participants_list), 200

    # ---------------------------------------------------------

    @staticmethod
    def delete_participant(db: Collection, id_participant: int):

        if id_participant:
            id_participant = int(id_participant)
            if db.delete_one({'id_participant': id_participant}):
                return OkCtrl.deleted('Participant')
            else:
                return jsonify({'error': 'Participant not found or not deleted', 'status': ParticipantCtrl.not_found}), 404
        else:
            return jsonify({'error': ParticipantCtrl.err_msg, 'status': ParticipantCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def delete_participant_form(db: Collection):
        id_participant = int(request.form.get('id_participant'))
        return ParticipantCtrl.delete_participant(db, id_participant)

    @staticmethod
    def put_participant_form(db: Collection):
        id_participant = int(request.form.get('id_participant'))
        return ParticipantCtrl.put_participant(db, id_participant)

    @staticmethod
    def put_participant(db: Collection, id_participant: int):
        if id_participant:
            id_participant = int(id_participant)
            name = request.form.get('name')
            surname = request.form.get('surname')
            age = request.form.get('age')
            nationality = request.form.get('nationality')
            if age:
                age = int(age)
            if not id_participant:
                return jsonify({'error': 'ID de participante requerido', 'status': ParticipantCtrl.bad_request}), 400

            participant_filter = {'id_participant': id_participant}

            update_fields = {}

            if name:
                update_fields['name'] = name
            if surname:
                update_fields['surname'] = surname
            if age:
                update_fields['age'] = age
            if nationality:
                update_fields['nationality'] = nationality

            change = {'$set': update_fields}

            result = db.update_one(participant_filter, change)
            if result.matched_count == 0:
                return jsonify({'error': 'Participante no encontrado', 'status': ParticipantCtrl.not_found}), 404
            elif result.modified_count == 0:
                return jsonify({'message': 'El participante ya está actualizado', 'status': '200 OK'}), 200

        return jsonify({'error': ParticipantCtrl.err_msg, 'status': ParticipantCtrl.bad_request}), 400

    # --------------------------------
