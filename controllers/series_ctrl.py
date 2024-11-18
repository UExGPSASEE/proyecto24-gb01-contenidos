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
        if idSeries:
            series = Series(idSeries, title, seasons, urlTitlePage, releaseDate, synopsis, description,
                          None, duration, language, category, character, participant, trailer)
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

