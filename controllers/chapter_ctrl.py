from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection

from database import get_next_sequence_value as get_next_sequence_value
from models.chapter import Chapter


class ChapterCtrl:

    err_msg = 'Missing data or incorrect method';
    chapter_not_found_msg = 'Capítulo no encontrado';
    not_found = '404 Not Found';
    bad_request = '400 Bad Request';

    @staticmethod
    def render_template(db: Collection):
        chaptersReceived = db.find()
        return render_template('Chapter.html', chapters=chaptersReceived)

    # ---------------------------------------------------------

    @staticmethod
    def add_chapter(db: Collection):
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
    def delete_chapter(db: Collection, idChapter: int):
        if idChapter:
            idChapter = int(idChapter)
            if db.delete_one({'idChapter': idChapter}):
                return redirect(url_for('chapters'))
            else:
                return jsonify({'error': ChapterCtrl.chapter_not_found_msg, 'status': ChapterCtrl.not_found}), 404
        else:
            return jsonify({'error': ChapterCtrl.err_msg, 'status': ChapterCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def delete_chapter_form(db: Collection):
        idChapter = int(request.form.get('idChapter'))
        return ChapterCtrl.delete_chapter(db, idChapter)

    @staticmethod
    def put_chapter_form(db: Collection):
        idChapter = int(request.form.get('idChapter'))
        return ChapterCtrl.put_chapter(db, idChapter)

    @staticmethod
    def put_chapter(db: Collection, idChapter):
        if idChapter:
            idChapter = int(idChapter)
            title = request.form.get('title')
            duration = request.form.get('duration')
            urlVideo = request.form.get('urlVideo')
            chapterNumber = request.form.get('chapterNumber')

            if not idChapter:
                return jsonify({'error': 'Identificador de capítulo requerido', 'status': ChapterCtrl.bad_request}), 400

            chapter_filter = {'idChapter': idChapter}

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

            result = db.update_one(chapter_filter, change)
            if result.matched_count == 0:
                return jsonify({'error': ChapterCtrl.chapter_not_found_msg, 'status': ChapterCtrl.not_found}), 404
            elif result.modified_count == 0:
                return jsonify({'message': 'El capítulo ya está actualizado', 'status': '200 OK'}), 200

        return jsonify({'error': ChapterCtrl.err_msg, 'status': ChapterCtrl.bad_request}), 400

    # --------------------------------

    @staticmethod
    def get_chapter_by_id(db: Collection, idChapter):
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
                return jsonify({'error': ChapterCtrl.chapter_not_found_msg, 'status': ChapterCtrl.not_found}), 404

        else:
            return jsonify({'error': ChapterCtrl.err_msg, 'status': ChapterCtrl.bad_request}), 400
