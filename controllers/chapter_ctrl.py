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
        chapter_title = request.form.get('title')
        duration = int(request.form.get('duration'))
        urlVideo = request.form.get('urlVideo')
        chapterNumber = int(request.form.get('chapterNumber'))
        if idChapter:
            chapter = Chapter(idChapter, chapter_title, duration, urlVideo, chapterNumber)
            db.insert_one(chapter.toDBCollection())
            return redirect(url_for('chapters'))
        else:
            return jsonify({'error': 'Chapter not found or not added', 'status':'404 Not Found'}), 404

# ---------------------------------------------------------
    @staticmethod
    def delete_chapter(db: Collection):
        if request.form.get('_method') == 'DELETE':
            chapter_id = int(request.form['idChapter'])
            if chapter_id and db.delete_one({'idChapter': chapter_id}):
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
            chapter_id = int(request.form.get('idChapter'))
            chapter_title = request.form.get('title')
            duration = request.form.get('duration')
            urlVideo = request.form.get('urlVideo')
            chapterNumber = request.form.get('chapterNumber')

            if not chapter_id:
                return jsonify({'error': 'ID de tráiler requerido', 'status': '400 Bad Request'}), 400

            filter = {'idChapter': chapter_id}

            update_fields = {}

            if chapter_title:
                update_fields['title'] = chapter_title
            if duration:
                update_fields['duration'] = int(duration)
            if urlVideo:
                update_fields['urlVideo'] = urlVideo
            if chapterNumber:
                update_fields['chapterNumber'] = int(chapterNumber)

            change = {'$set': update_fields}

            result = db.update_one(filter, change)
            if result.matched_count == 0:
                return jsonify({'error': 'Tráiler no encontrada', 'status': '404 Not Found'}), 404
            elif result.modified_count == 0:
                return jsonify({'message': 'La tráiler ya está actualizada', 'status': '200 OK'}), 200

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
            matching_chapter = db.find({'idChapter': idChapter})
            if matching_chapter:
                chapterFound = [
                {
                    'idChapter' : chapter.get('idCategory'),
                    'title' : chapter.get('title'),
                    'urlVideo' : chapter.get('urlVideo'),
                    'duration' : chapter.get('duration'),
                    'chapterNumber' : chapter.get('chapterNumber')
                }
                for chapter in matching_chapter
                ]
                return jsonify(chapterFound), 200
            else:
                return jsonify({'error': 'Chapter not found', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400