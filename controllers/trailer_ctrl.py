from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection

from database import get_next_sequence_value as get_next_sequence_value
from models.trailer import Trailer
from controllers.ok_ctrl import OkCtrl


class TrailerCtrl:

    err_msg = 'Missing data or incorrect method';
    not_found = '404 Not Found';
    bad_request = '400 Bad Request';

    @staticmethod
    def render_template(db: Collection):
        trailers_received = db.find()
        return render_template('Trailer.html', trailers=trailers_received)

    # ---------------------------------------------------------

    @staticmethod
    def add_trailer(db: Collection):
        id_trailer = int(get_next_sequence_value(db, "id_trailer"))
        title = request.form.get('title')
        duration = request.form.get('duration')
        url_video = request.form.get('url_video')
        if id_trailer:
            trailer = Trailer(id_trailer, title, duration, url_video, None, None, None, None)
            db.insert_one(trailer.to_db_collection())
            return OkCtrl.added('Trailer')
        else:
            return jsonify({'error': 'Tráiler no añadido', 'status': TrailerCtrl.not_found}), 404

    # ---------------------------------------------------------

    @staticmethod
    def get_trailer_by_id(db: Collection, id_trailer: int):
        if id_trailer:
            id_trailer = int(id_trailer)
            matching_trailer = db.find({'id_trailer': id_trailer})
            trailer_found = [
                {
                    'id_trailer': trailer.get('id_trailer'),
                    'title': trailer.get('title'),
                    'duration': trailer.get('duration'),
                    'url_video': trailer.get('url_video'),
                    'languages': trailer.get('languages'),
                    'categories': trailer.get('categories'),
                    'characters': trailer.get('characters'),
                    'participants': trailer.get('participants'),
                }
                for trailer in matching_trailer
            ]
            if trailer_found.__len__()>0:
                return jsonify(trailer_found), 200
            else:
                return jsonify({'error': 'Tráiler no encontrado', 'status': TrailerCtrl.not_found}), 404
        else:
            return jsonify({'error': TrailerCtrl.err_msg, 'status': TrailerCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def delete_trailer(db: Collection, id_trailer: int):
        if id_trailer:
            id_trailer = int(id_trailer)
            if db.delete_one({'id_trailer': id_trailer}):
                return OkCtrl.deleted('Trailer')
            else:
                return jsonify({'error': 'Trailer not found or not deleted', 'status': TrailerCtrl.not_found}), 404
        else:
            return jsonify({'error': TrailerCtrl.err_msg, 'status': TrailerCtrl.bad_request}), 400

    @staticmethod
    def delete_trailer_form(db: Collection):
        id_trailer = int(request.form['id_trailer'])
        return TrailerCtrl.delete_trailer(db, id_trailer)

    # ---------------------------------------------------------

    @staticmethod
    def put_trailer_form(db: Collection):
        id_trailer = int(request.form['id_trailer'])
        return TrailerCtrl.put_trailer(db, id_trailer)

    @staticmethod
    def put_trailer(db: Collection, id_trailer: int):
        if id_trailer:
            id_trailer = int(id_trailer)
            trailerTitle = request.form.get('title')
            duration = request.form.get('duration')
            url_video = request.form.get('url_video')

            if not id_trailer:
                return jsonify({'error': 'Identificador de tráiler requerido', 'status': TrailerCtrl.bad_request}), 400

            filter_dict = {'id_trailer': id_trailer}
            update_fields = {}

            if trailerTitle:
                update_fields['title'] = trailerTitle
            if duration:
                update_fields['duration'] = int(duration)
            if url_video:
                update_fields['url_video'] = url_video

            change = {'$set': update_fields}
            return TrailerCtrl.update_trailer(trailers, filter_dict, change)

        return jsonify({'error': TrailerCtrl.err_msg, 'status': TrailerCtrl.bad_request}), 400

# --------------------------------

    @staticmethod
    def put_category_into_trailer(trailers: Collection, categories: Collection, id_trailer: int):
        id_category = request.args.get('id_category')
        if id_category:
            id_category = int(id_category)
            if categories.find({'id_category': id_category}):
                filter_dict = {'id_trailer': int(id_trailer)}
                change = {'$addToSet': {'categories': id_category}}
                return TrailerCtrl.update_trailer(trailers, filter_dict, change)
            else:
                return jsonify({'error': 'No category was found', 'status': TrailerCtrl.not_found}), 400
        else:
            return jsonify({'error': TrailerCtrl.err_msg, 'status': TrailerCtrl.bad_request}), 400

    @staticmethod
    def delete_category_from_trailer(trailers: Collection, id_trailer: int):
        id_category = request.args.get('id_category')
        if id_category:
            id_category = int(id_category)
            filter_dict = {'id_trailer': int(id_trailer)}
            change = {'$pull': {'categories': id_category}}
            return TrailerCtrl.update_trailer(trailers, filter_dict, change)
        else:
            return jsonify({'error': TrailerCtrl.err_msg, 'status': TrailerCtrl.bad_request}), 400

    @staticmethod
    def update_trailer(db: Collection, filter_dict: dict[str, int], change_dict: dict[str, dict]):
        result = db.update_one(filter_dict, change_dict)
        print(result)
        if result.matched_count == 0:
            return jsonify({'error': 'Trailer not found or not updated', 'status': TrailerCtrl.not_found}), 404
        elif result.modified_count == 0:
            return jsonify({'message': 'There was no nothing to be updated or deleted', 'status': '200 OK'}), 200
        return OkCtrl.updated('Trailer')
