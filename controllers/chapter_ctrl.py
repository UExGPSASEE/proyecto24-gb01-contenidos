from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection

from database import get_next_sequence_value as get_next_sequence_value
from models.chapter import Chapter
from controllers.ok_ctrl import OkCtrl


class ChapterCtrl:

    err_msg = 'Missing data or incorrect method';
    chapter_not_found_msg = 'Capítulo no encontrado';
    not_found = '404 Not Found';
    bad_request = '400 Bad Request';

    @staticmethod
    def render_template(db: Collection):
        chapters_received = db.find()
        return render_template('Chapter.html', chapters=chapters_received)

    # ---------------------------------------------------------

    @staticmethod
    def add_chapter(db: Collection):
        id_chapter = int(get_next_sequence_value(db, "id_chapter"))
        title = request.form.get('title')
        duration = request.form.get('duration')
        url_video = request.form.get('url_video')
        chapter_number = int(request.form.get('chapter_number'))
        if id_chapter:
            chapter = Chapter(id_chapter, title, duration, url_video, chapter_number)
            db.insert_one(chapter.to_db_collection())
            return OkCtrl.added('Chapter')
        else:
            return jsonify({'error': 'Capítulo no añadido', 'status': ChapterCtrl.not_found}), 404

    # ---------------------------------------------------------
    @staticmethod
    def delete_chapter(db: Collection, id_chapter: int):
        if id_chapter:
            id_chapter = int(id_chapter)
            if db.delete_one({'id_chapter': id_chapter}):
                return OkCtrl.deleted('Chapter')
            else:
                return jsonify({'error': ChapterCtrl.chapter_not_found_msg, 'status': ChapterCtrl.not_found}), 404
        else:
            return jsonify({'error': ChapterCtrl.err_msg, 'status': ChapterCtrl.bad_request}), 400

    # ---------------------------------------------------------

    @staticmethod
    def delete_chapter_form(db: Collection):
        id_chapter = int(request.form.get('id_chapter'))
        return ChapterCtrl.delete_chapter(db, id_chapter)

    @staticmethod
    def put_chapter_form(db: Collection):
        id_chapter = int(request.form.get('id_chapter'))
        return ChapterCtrl.put_chapter(db, id_chapter)

    @staticmethod
    def put_chapter(db: Collection, id_chapter):
        if id_chapter:
            id_chapter = int(id_chapter)
            title = request.form.get('title')
            duration = request.form.get('duration')
            url_video = request.form.get('url_video')
            chapter_number = request.form.get('chapter_number')

            if not id_chapter:
                return jsonify({'error': 'Identificador de capítulo requerido', 'status': ChapterCtrl.bad_request}), 400

            chapter_filter = {'id_chapter': id_chapter}

            update_fields = {}

            if title:
                update_fields['title'] = title
            if duration:
                update_fields['duration'] = int(duration)
            if url_video:
                update_fields['url_video'] = url_video
            if chapter_number:
                update_fields['chapter_number'] = int(chapter_number)

            change = {'$set': update_fields}

            result = db.update_one(chapter_filter, change)
            if result.matched_count == 0:
                return jsonify({'error': ChapterCtrl.chapter_not_found_msg, 'status': ChapterCtrl.not_found}), 404
            elif result.modified_count == 0:
                return jsonify({'message': 'El capítulo ya está actualizado', 'status': '200 OK'}), 200
            else:
                return jsonify({'message': 'Capítulo actualizado', 'status': '200 OK'}), 200

        return jsonify({'error': ChapterCtrl.err_msg, 'status': ChapterCtrl.bad_request}), 400

    # --------------------------------

    @staticmethod
    def get_chapter_by_id(db: Collection, id_chapter):
        if id_chapter:
            id_chapter = int(id_chapter)
            matching_chapter = db.find({'id_chapter': id_chapter})
            chapterFound = [
                {
                    'id_chapter': chapter.get('id_chapter'),
                    'title': chapter.get('title'),
                    'url_video': chapter.get('url_video'),
                    'duration': chapter.get('duration'),
                    'chapter_number': chapter.get('chapter_number')
                }
                for chapter in matching_chapter
            ]
            if chapterFound.__len__() > 0:
                return jsonify(chapterFound), 200
            else:
                return jsonify({'error': ChapterCtrl.chapter_not_found_msg, 'status': ChapterCtrl.not_found}), 404

        else:
            return jsonify({'error': ChapterCtrl.err_msg, 'status': ChapterCtrl.bad_request}), 400
