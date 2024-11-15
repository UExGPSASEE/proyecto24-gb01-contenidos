from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection
from models.movie import Movie

class MovieCtrl:
    @staticmethod
    def render_template(db: Collection):
        moviesReceived = db.find()
        return render_template('Movie.html', movies=moviesReceived)

    @staticmethod        
    def get_next_sequence_value(db: Collection, sequence_name):        
        counter = db.find_one({"_id": sequence_name})

        if counter is None:       
            db.insert_one({"_id": sequence_name, "sequence_value": 1})
            return 1
        
        updated_counter = db.find_one_and_update(
            {"_id": sequence_name},
            {"$inc": {"sequence_value": 1}},
            return_document=True
        )
        return updated_counter["sequence_value"]
    
# ---------------------------------------------------------

    @staticmethod
    def addMovie(db: Collection):
        idMovie = MovieCtrl.get_next_sequence_value(db,"idMovie")
        title = request.form['title']
        urlVideo = request.form['urlVideo']
        urlTitlePage = request.form['urlTitlePage']
        releaseDate = request.form['releaseDate']
        synopsis = request.form['synopsis']
        description = request.form['description']
        duration = request.form['duration']
        language = request.form.getlist('language[]')
        category = request.form.getlist('category[]')
        character = request.form.getlist('character[]')
        participant = request.form.getlist('participant[]')
        trailer = request.form['trailer']
        if idMovie:
            movie = Movie(idMovie, title, urlVideo, urlTitlePage, releaseDate, synopsis, description,
                          None, duration, language, category, character, participant, trailer)
            db.insert_one(movie.toDBCollection())
            return redirect(url_for('movies'))
        else:
            return jsonify({'error': 'Movie not found or not added', 'status':'404 Not Found'}), 404

# ---------------------------------------------------------

    @staticmethod
    def getMovieById(db: Collection):
        idMovie = int(request.args.get('idMovie'))
        if idMovie:
            matching_movie = db.find({'idMovie': idMovie})
            if matching_movie:
                movieFound = [
                {
                    'idMovie' : movie.get('idMovie'),
                    'title' : movie.get('title'),
                    'urlVideo' : movie.get('urlVideo'),
                    'urlTitlePage' : movie.get('urlTitlePage'),
                    'releaseDate' : movie.get('releaseDate'),
                    'synopsis' : movie.get('synopsis'),
                    'description' : movie.get('description'),
                    'isSuscription' : movie.get('isSuscription'),
                    'duration' : movie.get('duration'),
                    'language' : movie.get('language'),
                    'category' : movie.get('category'),
                    'character' : movie.get('character'),
                    'participant' : movie.get('participant'),
                    'trailer' : movie.get('trailer'),
                }
                for movie in matching_movie
                ]
                return jsonify(movieFound), 200
            else:
                return jsonify({'error': 'Movie not found', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

# ---------------------------------------------------------

    @staticmethod
    def delete_movie(db: Collection):
        movie_name = request.form['name']
        db.delete_one({'name': movie_name})
        if request.form.get('_method') == 'DELETE':
            movie_name = request.form['name']
            result = db.delete_one({'name': movie_name})
            if result.deleted_count == 1:
                print("Delete ok")
                return redirect(url_for('movies'))
            else:
                print("Delete failed")
                return redirect(url_for('movies'))
        else:
            return redirect(url_for('movies'))

# ---------------------------------------------------------

    @staticmethod
    def put_movie(db: Collection, movies_name):
        data = request.json

        if 'name' in data:
            result = db.update_one(data)
            if result.modified_count == 1:
                return jsonify({'message': f'Movie {movies_name} updated.'}), 200
            else:
                return jsonify({'error': 'Movie not found or not updated'}), 404
        else:
            return jsonify({'error': 'Movie not found or not updated'}), 404

# ---------------------------------------------------------

