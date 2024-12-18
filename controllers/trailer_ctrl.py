from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection

from database import get_next_sequence_value as get_next_sequence_value
from models.trailer import Trailer


class TrailerCtrl:

    err_msg = 'Missing data or incorrect method';
    not_found = '404 Not Found';
    bad_request = '400 Bad Request';

    @staticmethod
    def render_template(db: Collection):
        trailersReceived = db.find()
        return render_template('Trailer.html', trailers=trailersReceived)

    # ---------------------------------------------------------

    @staticmethod
    def addTrailer(db: Collection):
        idTrailer = int(get_next_sequence_value(db, "idTrailer"))
        title = request.form.get('title')
        duration = request.form.get('duration')
        urlVideo = request.form.get('urlVideo')
        if idTrailer:
            trailer = Trailer(idTrailer, title, duration, urlVideo, None, None, None, None)
            db.insert_one(trailer.toDBCollection())
            return redirect(url_for('trailers'))
        else:
            return jsonify({'error': 'Tráiler no añadido', 'status': TrailerCtrl.not_found}), 404

    # ---------------------------------------------------------

    @staticmethod
    def getTrailerById(db: Collection, idTrailer: int):
        if idTrailer:
            idTrailer = int(idTrailer)
            matchingTrailer = db.find({'idTrailer': idTrailer})
            trailerFound = [
                {
                    'idTrailer': trailer.get('idTrailer'),
                    'title': trailer.get('title'),
                    'duration': trailer.get('duration'),
                    'urlVideo': trailer.get('urlVideo'),
                    'languages': trailer.get('languages'),
                    'categories': trailer.get('categories'),
                    'characters': trailer.get('characters'),
                    'participants': trailer.get('participants'),
                }
                for trailer in matchingTrailer
            ]
            if trailerFound.__len__()>0:
                return jsonify(trailerFound), 200
            else:
                return jsonify({'error': 'Tráiler no encontrado', 'status': TrailerCtrl.not_found}), 404
        else:
            return jsonify({'error': TrailerCtrl.err_msg, 'status': TrailerCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def deleteTrailer(db: Collection, idTrailer: int):
        if idTrailer:
            idTrailer = int(idTrailer)
            if db.delete_one({'idTrailer': idTrailer}):
                return redirect(url_for('trailers'))
            else:
                return jsonify({'error': 'Trailer not found or not deleted', 'status': TrailerCtrl.not_found}), 404
        else:
            return jsonify({'error': TrailerCtrl.err_msg, 'status': TrailerCtrl.bad_request}), 400

    @staticmethod
    def deleteTrailerForm(db: Collection):
        idTrailer = int(request.form['idTrailer'])
        return TrailerCtrl.deleteTrailer(db, idTrailer)

    # ---------------------------------------------------------

    @staticmethod
    def putTrailerForm(db: Collection):
        idTrailer = int(request.form['idTrailer'])
        return TrailerCtrl.putTrailer(db, idTrailer)

    @staticmethod
    def putTrailer(db: Collection, idTrailer: int):
        if idTrailer:
            idTrailer = int(idTrailer)
            trailerTitle = request.form.get('title')
            duration = request.form.get('duration')
            urlVideo = request.form.get('urlVideo')

            if not idTrailer:
                return jsonify({'error': 'Identificador de tráiler requerido', 'status': TrailerCtrl.bad_request}), 400

            filterDict = {'idTrailer': idTrailer}
            updateFields = {}

            if trailerTitle:
                updateFields['title'] = trailerTitle
            if duration:
                updateFields['duration'] = int(duration)
            if urlVideo:
                updateFields['urlVideo'] = urlVideo

            change = {'$set': updateFields}
            return TrailerCtrl.updateTrailer(trailers, filterDict, change)

        return jsonify({'error': TrailerCtrl.err_msg, 'status': TrailerCtrl.bad_request}), 400

# --------------------------------

    @staticmethod
    def putCategoryIntoTrailer(trailers: Collection, categories: Collection, idTrailer: int):
        idCategory = request.args.get('idCategory')
        if idCategory:
            idCategory = int(idCategory)
            if categories.find({'idCategory': idCategory}):
                filterDict = {'idTrailer': int(idTrailer)}
                change = {'$addToSet': {'categories': idCategory}}
                return TrailerCtrl.updateTrailer(trailers, filterDict, change)
            else:
                return jsonify({'error': 'No category was found', 'status': TrailerCtrl.not_found}), 400
        else:
            return jsonify({'error': TrailerCtrl.err_msg, 'status': TrailerCtrl.bad_request}), 400

    @staticmethod
    def deleteCategoryFromTrailer(trailers: Collection, idTrailer: int):
        idCategory = request.args.get('idCategory')
        if idCategory:
            idCategory = int(idCategory)
            filterDict = {'idTrailer': int(idTrailer)}
            change = {'$pull': {'categories': idCategory}}
            return TrailerCtrl.updateTrailer(trailers, filterDict, change)
        else:
            return jsonify({'error': TrailerCtrl.err_msg, 'status': TrailerCtrl.bad_request}), 400

    @staticmethod
    def updateTrailer(db: Collection, filterDict: dict[str, int], changeDict: dict[str, dict]):
        result = db.update_one(filterDict, changeDict)
        print(result)
        if result.matched_count == 0:
            return jsonify({'error': 'Trailer not found or not updated', 'status': TrailerCtrl.not_found}), 404
        elif result.modified_count == 0:
            return jsonify({'message': 'There was no nothing to be updated or deleted', 'status': '200 OK'}), 200
        return redirect(url_for('trailers'))
