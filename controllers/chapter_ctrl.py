from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection

from database import get_next_sequence_value as get_next_sequence_value
from models.chapter import Chapter


class ChapterCtrl:

    err_msg = 'Missing data or incorrect method';
    not_found = '404 Not Found';

    @staticmethod
    def render_template(db: Collection):
        chaptersReceived = db.find()
        return render_template('Chapter.html', chapters=chaptersReceived)

    # ---------------------------------------------------------

    @staticmethod
    def addChapter(db: Collection):
        idChapter = int(get_next_sequence_value(db, "idChapter"))
        title = request.form.get('title')
        duration = request.form.get('duration')
        urlVideo = request.form.get('urlVideo')
        chapterNumber = int(request.form.get('chapterNumber'))
        if idChapter:
            chapter = Chapter(idChapter, title, duration, urlVideo, chapterNumber)
            db.insert_one(chapter.toDBCollection())
            return redirect(url_for('chapters'))
        else:
            return jsonify({'error': 'Capítulo no añadido', 'status': ChapterCtrl.not_found}), 404

    # ---------------------------------------------------------
    @staticmethod
    def deleteChapter(db: Collection, idChapter: int):
        if idChapter:
            idChapter = int(idChapter)
            if db.delete_one({'idChapter': idChapter}):
                return redirect(url_for('chapters'))
            else:
                return jsonify({'error': 'Chapter not found or not deleted', 'status': ChapterCtrl.not_found}), 404
        else:
            return jsonify({'error': ChapterCtrl.err_msg, 'status': '400 Bad Request'}), 400

    # ---------------------------------------------------------

    @staticmethod
    def deleteChapterForm(db: Collection):
        idChapter = int(request.form.get('idChapter'))
        return ChapterCtrl.deleteChapter(db, idChapter)

    @staticmethod
    def putChapterForm(db: Collection):
        idChapter = int(request.form.get('idChapter'))
        return ChapterCtrl.putChapter(db, idChapter)

    @staticmethod
    def putChapter(db: Collection, idChapter):
        if idChapter:
            idChapter = int(idChapter)
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
                return jsonify({'error': 'Capítulo no encontrado', 'status': ChapterCtrl.not_found}), 404
            elif result.modified_count == 0:
                return jsonify({'message': 'El capítulo ya está actualizado', 'status': '200 OK'}), 200

        return jsonify({'error': ChapterCtrl.err_msg, 'status': '400 Bad Request'}), 400

    # --------------------------------

    @staticmethod
    def getChapterById(db: Collection, idChapter):
        if idChapter:
            idChapter = int(idChapter)
            matchingChapter = db.find({'idChapter': idChapter})
            chapterFound = [
                {
                    'idChapter': chapter.get('idChapter'),
                    'title': chapter.get('title'),
                    'urlVideo': chapter.get('urlVideo'),
                    'duration': chapter.get('duration'),
                    'chapterNumber': chapter.get('chapterNumber')
                }
                for chapter in matchingChapter
            ]
            if chapterFound.__len__() > 0:
                return jsonify(chapterFound), 200
            else:
                return jsonify({'error': 'Capítulo no encontrado', 'status': ChapterCtrl.not_found}), 404

        else:
            return jsonify({'error': ChapterCtrl.err_msg, 'status': '400 Bad Request'}), 400
