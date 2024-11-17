from flask import render_template, request, jsonify, redirect, url_for
from database import get_next_sequence_value as get_next_sequence_value
from pymongo.collection import Collection
from models.participant import Participant

class ParticipantCtrl:

    @staticmethod
    def render_template(db: Collection):
        participants = db['participants']
        participantsReceived = participants.find()
        return render_template('Participant.html', participants=participantsReceived)

    @staticmethod
    def addParticipant(db: Collection):
        idParticipant = get_next_sequence_value(db, "idParticipant")
        name = request.form.get('name')
        surname = request.form.get('surname')
        age = int(request.form.get('age'))
        nationality = request.form.get('nationality')

        if name:
            participant = Participant(idParticipant, name, surname, age, nationality)
            db.insert_one(participant.toDBCollection())

            return redirect(url_for('participants'))
        else:
            return jsonify({'error': 'Participant not found or not added', 'status': '404 Not Found'}), 404

    # ---------------------------------------------------------

    @staticmethod
    def getParticipantByName(db: Collection):
        name = request.args.get('name')
        if name:
            matching_participants = db.find({'name': name})
            participants_list = [
                {
                    'name': participant.get('name'),
                    'surname': participant.get('surname'),
                    'age': participant.get('age'),
                    'nationality': participant.get('nationality')
                }
                for participant in matching_participants
            ]

            return jsonify(participants_list), 200
        else:
            return jsonify({'error': 'Nombre no proporcionado'}), 400

    @staticmethod
    def getParticipantBySurname(db: Collection):
        surname = request.args.get('surname')

        if surname:
            matching_participants = db.find({'surname': surname})

            participants_list = [
                {
                    'name': participant.get('name'),
                    'surname': participant.get('surname'),
                    'age': participant.get('age'),
                    'nationality': participant.get('nationality')
                }
                for participant in matching_participants
            ]

            return jsonify(participants_list), 200
        else:
            return jsonify({'error': 'Apellido/s no proporcionados'}), 400

    @staticmethod
    def getParticipantByAge(db: Collection):
        age = int(request.args.get('age'))

        if age:
            matching_participants = db.find({'age': age})

            participants_list = [
                {
                    'name': participant.get('name'),
                    'surname': participant.get('surname'),
                    'age': participant.get('age'),
                    'nationality': participant.get('nationality')
                }
                for participant in matching_participants
            ]

            return jsonify(participants_list), 200
        else:
            return jsonify({'error': 'Edad no proporcionada'}), 400

    @staticmethod
    def getParticipantByNationality(db: Collection):
        nationality = request.args.get('nationality')
        if nationality:
            matching_participants = db.find({'nationality': nationality})
            participants_list = [
                {
                    'name': participant.get('name'),
                    'surname': participant.get('surname'),
                    'age': participant.get('age'),
                    'nationality': participant.get('nationality')
                }
                for participant in matching_participants
            ]

            return jsonify(participants_list), 200
        else:
            return jsonify({'error': 'Nacionalidad no proporcionada'}), 400

    @staticmethod
    def getParticipantById(db: Collection):
        id = request.args.get('participant_id')
        participant_id = int(id)
        print(id)
        if id:
            matching_participant = db.find({'participant_id': participant_id})
            participants_list = [
                {
                    'participant_id': participant.get('participant_id'),
                    'name': participant.get('name'),
                    'surname': participant.get('surname'),
                    'age': participant.get('age'),
                    'nationality': participant.get('nationality')
                }
                for participant in matching_participant
            ]
            return jsonify(participants_list), 200
        else:
            return jsonify({'error': 'Id no proporcionado'}), 400


    @staticmethod
    def getAllParticipants(db: Collection):
        allParticipants = db.find()
        participants_list = [
            {
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
    def deleteParticipant(db: Collection):
        if request.form.get('_method') == 'DELETE':
            participant_id = int(request.form['participant_id'])
            if participant_id and db.delete_one({'participant_id': participant_id}):
                print("Delete ok")
                return redirect(url_for('participants'))
            else:
                print("Delete failed")
                return redirect(url_for('participants'))
        else:
            return redirect(url_for('participants'))

    # ---------------------------------------------------------

    @staticmethod
    def updateParticipant(db: Collection):
        if request.form.get('_method') != 'PUT':
            return jsonify({'error': 'No se puede actualizar', 'status': '400 Bad Request'}), 400
        try:
            participant_id = int(request.form.get('participant_id'))
            name = request.form.get('name')
            surname = request.form.get('surname')
            age_value = str(request.form.get('age'))
            if age_value:
                age = int(age_value)
                print(age)
            else:
                age = None  # O simplemente ignóralo si no necesitas asignarlo
            nationality = request.form.get('nationality')

            if not participant_id:
                return jsonify({'error': 'ID de participante requerido', 'status': '400 Bad Request'}), 400

            filter = {'participant_id': participant_id}

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

            result = db.update_one(filter, change)
            if result.matched_count == 0:
                return jsonify({'error': 'Participante no encontrado', 'status': '404 Not Found'}), 404
            elif result.modified_count == 0:
                return jsonify({'message': 'El participante ya está actualizado', 'status': '200 OK'}), 200

            return redirect(url_for('participants'))

        except ValueError:
            return jsonify({'error': 'Datos inválidos', 'status': '400 Bad Request'}), 400

        except Exception as e:
            return jsonify(
                {'error': f'Error interno del servidor: {str(e)}', 'status': '500 Internal Server Error'}
            ), 500

    # --------------------------------
