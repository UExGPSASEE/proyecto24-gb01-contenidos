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
        trailer_title = request.form.get('title')
        duration = request.form.get('duration')
        urlVideo = request.form.get('urlVideo')
        language = request.form.getlist('language[]')
        category = request.form.getlist('category[]')
        character = request.form.getlist('character[]')
        participant = request.form.getlist('participant[]')
        if idTrailer:
            trailer = Trailer(idTrailer, trailer_title, duration, urlVideo, language, category, character, participant)
            db.insert_one(trailer.toDBCollection())
            return redirect(url_for('trailers'))
        else:
            return jsonify({'error': 'Trailer not found or not added', 'status':'404 Not Found'}), 404

# ---------------------------------------------------------
    @staticmethod
    def delete_trailer(db: Collection):
        if request.form.get('_method') == 'DELETE':
            trailer_id = int(request.form['id'])
            if trailer_id and db.delete_one({'idTrailer': trailer_id}):
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
            trailer_id = int(request.form.get('id'))
            trailer_title = request.form.get('title')
            duration = request.form.get('duration')
            urlVideo = request.form.get('urlVideo')
            language = request.form.getlist('language[]')
            category = request.form.getlist('category[]')
            character = request.form.getlist('character[]')
            participant = request.form.getlist('participant[]')

            if not trailer_id:
                return jsonify({'error': 'ID de tráiler requerido', 'status': '400 Bad Request'}), 400

            filter = {'idTrailer': trailer_id}

            update_fields = {}

            if trailer_title:
                update_fields['title'] = trailer_title
            if duration:
                update_fields['duration'] = int(duration)  # Convertir a entero si aplica
            if urlVideo:
                update_fields['urlVideo'] = urlVideo
            if language:
                update_fields['language'] = language
            if category:
                update_fields['category'] = category
            if character:
                update_fields['character'] = character
            if participant:
                update_fields['participant'] = participant

            change = {'$set': update_fields}

            result = db.update_one(filter, change)
            if result.matched_count == 0:
                return jsonify({'error': 'Tráiler no encontrado', 'status': '404 Not Found'}), 404
            elif result.modified_count == 0:
                return jsonify({'message': 'El tráiler ya está actualizado', 'status': '200 OK'}), 200

            # Redirigir a la lista de tráileres
            return redirect(url_for('trailers'))

        except ValueError:
            return jsonify({'error': 'Datos inválidos', 'status': '400 Bad Request'}), 400

        except Exception as e:
            return jsonify(
                {'error': f'Error interno del servidor: {str(e)}', 'status': '500 Internal Server Error'}
            ), 500

# --------------------------------