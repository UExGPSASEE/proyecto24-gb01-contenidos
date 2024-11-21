from flask import render_template, request, jsonify, redirect, url_for
from database import get_next_sequence_value as get_next_sequence_value
from pymongo.collection import Collection
from models.trailer import Trailer

class TrailerCtrl:
    @staticmethod
    def render_template(db: Collection):
        trailersReceived = db.find()
        return render_template('Trailer.html', trailers=trailersReceived)

# ---------------------------------------------------------

    @staticmethod
    def addTrailer(db: Collection):
        idTrailer = get_next_sequence_value(db,"idTrailer")
        title = request.form.get('title')
        duration = request.form.get('duration')
        urlVideo = request.form.get('urlVideo')
        language = request.form.getlist('language[]')
        category = request.form.getlist('category[]')
        character = request.form.getlist('character[]')
        participant = request.form.getlist('participant[]')
        if idTrailer:
            trailer = Trailer(idTrailer, title, duration, urlVideo, language, category, character, participant)
            db.insert_one(trailer.toDBCollection())
            return redirect(url_for('trailers'))
        else:
            return jsonify({'error': 'Tráiler no añadido', 'status':'404 Not Found'}), 404

# ---------------------------------------------------------

    @staticmethod
    def getTrailerById(db: Collection):
        idTrailer = int(request.args.get('idTrailer'))
        if idTrailer:
            matchingTrailer = db.find({'idTrailer': idTrailer})
            if matchingTrailer:
                trailerFound = [
                {
                    'idTrailer' : trailer.get('idTrailer'),
                    'title' : trailer.get('title'),
                    'duration' : trailer.get('duration'),
                    'urlVideo' : trailer.get('urlVideo'),
                    'language' : trailer.get('language'),
                    'category' : trailer.get('category'),
                    'character' : trailer.get('character'),
                    'participant' : trailer.get('participant'),
                }
                for trailer in matchingTrailer
                ]
                return jsonify(trailerFound), 200
            else:
                return jsonify({'error': 'Tráiler no encontrado', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Falta de datos o método incorrecto', 'status': '400 Bad Request'}), 400

# ---------------------------------------------------------

    @staticmethod
    def delete_trailer(db: Collection):
        if request.form.get('_method') == 'DELETE':
            idTrailer = int(request.form['idTrailer'])
            if idTrailer and db.delete_one({'idTrailer': idTrailer}):
                print("Delete ok")
                return redirect(url_for('trailers'))
            else:
                print("Delete failed")
                return redirect(url_for('trailers'))
        else:
            return redirect(url_for('trailers'))

# ---------------------------------------------------------

    @staticmethod
    def put_trailer(db: Collection):
        if request.form.get('_method') != 'PUT':
            return jsonify({'error': 'No se puede actualizar', 'status': '400 Bad Request'}), 400
        try:
            idTrailer = int(request.form.get('idTrailer'))
            trailerTitle = request.form.get('title')
            duration = request.form.get('duration')
            urlVideo = request.form.get('urlVideo')
            language = request.form.getlist('language[]')
            category = request.form.getlist('category[]')
            character = request.form.getlist('character[]')
            participant = request.form.getlist('participant[]')

            if not idTrailer:
                return jsonify({'error': 'Identificador de tráiler requerido', 'status': '400 Bad Request'}), 400

            filter = {'idTrailer': idTrailer}

            updateFields = {}

            if trailerTitle:
                updateFields['title'] = trailerTitle
            if duration:
                updateFields['duration'] = int(duration)
            if urlVideo:
                updateFields['urlVideo'] = urlVideo
            if language:
                updateFields['language'] = language
            if category:
                updateFields['category'] = category
            if character:
                updateFields['character'] = character
            if participant:
                updateFields['participant'] = participant

            change = {'$set': updateFields}

            result = db.update_one(filter, change)
            if result.matched_count == 0:
                return jsonify({'error': 'Tráiler no encontrado', 'status': '404 Not Found'}), 404
            elif result.modified_count == 0:
                return jsonify({'message': 'El tráiler ya está actualizado', 'status': '200 OK'}), 200

            return redirect(url_for('trailers'))

        except ValueError:
            return jsonify({'error': 'Datos inválidos', 'status': '400 Bad Request'}), 400

        except Exception as e:
            return jsonify(
                {'error': f'Error interno del servidor: {str(e)}', 'status': '500 Internal Server Error'}
            ), 500

# --------------------------------
