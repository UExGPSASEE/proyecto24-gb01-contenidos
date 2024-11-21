from flask import render_template, request, jsonify, redirect, url_for
from database import get_next_sequence_value as get_next_sequence_value
from pymongo.collection import Collection
from models.chapter import Chapter

class ChapterCtrl:
    @staticmethod
    def render_template(db: Collection):
        chaptersReceived = db.find()
        return render_template('Chapter.html', chapters=chaptersReceived)

# ---------------------------------------------------------

    @staticmethod
    def addChapter(db: Collection):
        idChapter = get_next_sequence_value(db,"idChapter")
        title = request.form.get('title')
        duration = request.form.get('duration')
        urlVideo = request.form.get('urlVideo')
        chapterNumber = int(request.form.get('chapterNumber'))
        if idChapter:
            chapter = Chapter(idChapter, title, duration, urlVideo, chapterNumber)
            db.insert_one(chapter.toDBCollection())
            return redirect(url_for('chapters'))
        else:
            return jsonify({'error': 'Capítulo no añadido', 'status':'404 Not Found'}), 404

# ---------------------------------------------------------
    @staticmethod
    def delete_chapter(db: Collection):
        if request.form.get('_method') == 'DELETE':
            idChapter = int(request.form['idChapter'])
            if idChapter and db.delete_one({'idChapter': idChapter}):
                print("Delete ok")
                return redirect(url_for('chapters'))
            else:
                print("Delete failed")
                return redirect(url_for('chapters'))
        else:
            return redirect(url_for('chapters'))

# ---------------------------------------------------------

    @staticmethod
    def put_chapter(db: Collection):
        if request.form.get('_method') != 'PUT':
            return jsonify({'error': 'No se puede actualizar', 'status': '400 Bad Request'}), 400
        try:
            idChapter = int(request.form.get('idChapter'))
            title = request.form.get('title')
            duration = request.form.get('duration')
            urlVideo = request.form.get('urlVideo')
            chapterNumber = request.form.get('chapterNumber')

            if not idChapter:
                return jsonify({'error': 'Identificador de capítulo requerido', 'status': '400 Bad Request'}), 400

            filter = {'idChapter': idChapter}

            updateFields = {}

            if title:
                updateFields['title'] = title
            if duration:
                updateFields['duration'] = int(duration)
            if urlVideo:
                updateFields['urlVideo'] = urlVideo
            if chapterNumber:
                updateFields['chapterNumber'] = int(chapterNumber)

            change = {'$set': updateFields}

            result = db.update_one(filter, change)
            if result.matched_count == 0:
                return jsonify({'error': 'Capítulo no encontrado', 'status': '404 Not Found'}), 404
            elif result.modified_count == 0:
                return jsonify({'message': 'El capítulo ya está actualizado', 'status': '200 OK'}), 200

            return redirect(url_for('chapters'))

        except ValueError:
            return jsonify({'error': 'Datos inválidos', 'status': '400 Bad Request'}), 400

        except Exception as e:
            return jsonify(
                {'error': f'Error interno del servidor: {str(e)}', 'status': '500 Internal Server Error'}
            ), 500

# --------------------------------

    @staticmethod
    def getChapterById(db: Collection):
        idChapter = int(request.args.get('idChapter'))
        if idChapter:
            matchingChapter = db.find({'idChapter': idChapter})
            if matchingChapter:
                chapterFound = [
                {
                    'idChapter' : chapter.get('idChapter'),
                    'title' : chapter.get('title'),
                    'urlVideo' : chapter.get('urlVideo'),
                    'duration' : chapter.get('duration'),
                    'chapterNumber' : chapter.get('chapterNumber')
                }
                for chapter in matchingChapter
                ]
                return jsonify(chapterFound), 200
            else:
                return jsonify({'error': 'Capítulo no encontrado', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Falta de datos o método incorrecto', 'status': '400 Bad Request'}), 400
