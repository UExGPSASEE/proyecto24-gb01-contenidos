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
        suscription = request.form.get('isSuscription')

        if suscription:
            if suscription == True:
                isSuscription = True
            else: isSuscription = False

        if idSeries:
            series = Series(idSeries, title, seasons, urlTitlePage, releaseDate, synopsis, description,
                          isSuscription, duration, language, category, character, participant, trailer)
            db.insert_one(series.toDBCollection())
            return redirect(url_for('series'))
        else:
            return jsonify({'error': 'Series not found or not added', 'status':'404 Not Found'}), 404

# --------------------------------------------------------------

    @staticmethod
    def getAllSeries(db: Collection):
        allSeries = db.find()
        series_list = [
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
            for series in allSeries
        ]
        return jsonify(series_list), 200

# --------------------------------------------------------------

    @staticmethod
    def getSeriesByTitle(db: Collection):
        title = request.args.get('title')
        if title:
            matching_series = db.find({'title': title})
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
                return jsonify({'error': 'Series not found', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

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
                return jsonify({'error': 'ID de serie requerido', 'status': '400 Bad Request'}), 400

            filter = {'idSeries': idSeries}

            update_fields = {}

            if title:
                update_fields['title'] = title
            if duration:
                update_fields['duration'] = int(duration)  # Convertir a entero si aplica
            if seasons:
                update_fields['seasons'] = seasons
            if urlTitlePage:
                update_fields['urlTitlePage'] = urlTitlePage
            if releaseDate:
                update_fields['releaseDate'] = releaseDate
            if synopsis:
                update_fields['synopsis'] = synopsis
            if description:
                update_fields['description'] = description
            if language:
                update_fields['language'] = language
            if category:
                update_fields['category'] = category
            if character:
                update_fields['character'] = character
            if participant:
                update_fields['participant'] = participant
            if trailer:
                update_fields['trailer'] = trailer
            if isSuscription:
                if isSuscription == True:
                    update_fields['isSuscription'] = True
                else: update_fields['isSuscription'] = False

            change = {'$set': update_fields}

            result = db.update_one(filter, change)
            if result.matched_count == 0:
                return jsonify({'error': 'Serie no encontrada', 'status': '404 Not Found'}), 404
            elif result.modified_count == 0:
                return jsonify({'message': 'La serie ya está actualizada', 'status': '200 OK'}), 200

            # Redirigir a la lista de películas
            return redirect(url_for('series'))

        except ValueError:
            return jsonify({'error': 'Datos inválidos', 'status': '400 Bad Request'}), 400

        except Exception as e:
            return jsonify(
                {'error': f'Error interno del servidor: {str(e)}', 'status': '500 Internal Server Error'}
            ), 500
