import database as dbase
from flask import Flask, render_template, request, jsonify, redirect, url_for
from controllers.movie_ctrl import MovieCtrl
from controllers.category_ctrl import CategoryCtrl
from controllers.trailer_ctrl import TrailerCtrl
from participant import Participant

db = dbase.conexionMongoDB()

app = Flask(__name__)
# -------------------------------------------------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html')
# -------------------------------------------------------------------------------------------------------
@app.route('/movies')
def movies():
    return MovieCtrl.render_template(db['movies'])

@app.route('/movies/addMovie', methods=['POST'])
def addMovie():
    return MovieCtrl.addMovie(db['movies'])

@app.route('/movies/deleteMovie', methods=['POST'])
def deleteMovie():
    return MovieCtrl.delete_movie(db['movies'])

@app.route('/movies/movieFound', methods=['GET'])
def getMovieById():
    return MovieCtrl.getMovieById(db['movies'])

@app.route('/movies/updateMovie', methods=['POST'])
def putMovie():
    return MovieCtrl.put_movie(db['movies'])

# -------------------------------------------------------------------------------------------------------
@app.route('/trailers')
def trailers():
    return TrailerCtrl.render_template(db['trailers'])

@app.route('/trailers/addTrailer', methods=['POST'])
def addTrailer():
    return TrailerCtrl.addTrailer(db['trailers'])

@app.route('/trailers/deleteTrailer', methods=['POST'])
def deleteTrailer():
    return TrailerCtrl.delete_trailer(db['trailers'])

# @app.route('/trailers/trailerFound', methods=['GET'])
# def getTrailerById():
#     return TrailerCtrl.getTrailerById(db['trailers'])

@app.route('/trailers/updateTrailer', methods=['POST'])
def putTrailer():
    return TrailerCtrl.put_trailer(db['trailers'])

# -------------------------------------------------------------------------------------------------------

@app.route('/categories')
def categories():
    categories = db['categories']
    categoriesReceived = categories.find()
    return render_template('Category.html', categories=categoriesReceived)

@app.route('/categories/categoryAdded', methods=['POST'])
def addCategory():
    return CategoryCtrl.addCategory(db['categories'])

@app.route('/categories/categoriesListed', methods=['GET'])
def getAllCategories():
    return CategoryCtrl.getAllCategories(db['categories'])

@app.route('/categories/categoryFound', methods=['GET'])
def getCategoryById():
    return CategoryCtrl.getCategoryById(db['categories'])

# -------------------------------------------------------------------------------------------------------

def get_next_sequence_value(sequence_name):
    counter = db.participants_id.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"sequence_value": 1}},
        return_document=True
    )
    return counter["sequence_value"]

@app.route('/participants')
def participants():
    participants = db['participants']
    participantsReceived = participants.find()
    return render_template('Participant.html', participants=participantsReceived)

@app.route('/participants/addParticipant', methods=['POST'])
def addParticipant():
    participants = db['participants']
    name = request.form['name']
    surname = request.form['surname']
    age = request.form['age']
    nationality = request.form['nationality']

    unique_id = get_next_sequence_value("participant_id")

    if name:
        participant = Participant(unique_id, name, surname, age, nationality)
        response = jsonify({
            'name': name
        })
        participants.insert_one(participant.toDBCollection())

        return redirect(url_for('participants'))
    else:
        return notFound()

@app.route('/participants/getParticipantByName', methods=['GET'])
def getParticipantByName():
    participants = db['participants']
    name = request.args.get('name')

    if name:
        matching_participants = participants.find({'name': name})

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

@app.route('/participants/getParticipantBySurname', methods=['GET'])
def getParticipantBySurname():
    participants = db['participants']
    surname = request.args.get('surname')

    if surname:
        matching_participants = participants.find({'surname': surname})

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

@app.route('/participants/getParticipantByAge', methods=['GET'])
def getParticipantByAge():
    participants = db['participants']
    age = request.args.get('age')

    if age:
        matching_participants = participants.find({'age': age})

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

@app.route('/participants/getParticipantByNationality', methods=['GET'])
def getParticipantByNationality():
    participants = db['participants']
    nationality = request.args.get('nationality')

    if nationality:
        matching_participants = participants.find({'nationality': nationality})

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

@app.route('/participants/getAllParticipants', methods=['GET'])
def getAllParticipants():
    participants = db['participants']
    allParticipants = participants.find()
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



@app.errorhandler(404)
def notFound(error=None):
    message = {
        'message': 'No encontrado' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(debug=True, port=8082)
