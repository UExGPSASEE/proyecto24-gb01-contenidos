from flask import render_template, request, jsonify, redirect, url_for
from database import get_next_sequence_value as get_next_sequence_value
from pymongo.collection import Collection
from models.series import Series

class SeriesCtrl:
    @staticmethod
    def render_template(db: Collection):
        seriesReceived = db.find()
        return render_template('Series.html', series=seriesReceived)

    # ---------------------------------------------------------

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
