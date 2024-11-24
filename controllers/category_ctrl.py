from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection

from database import get_next_sequence_value as get_next_sequence_value
from models.category import Category


class CategoryCtrl:

    @staticmethod
    def render_template(db: Collection):
        categoriesReceived = db.find()
        return render_template('Category.html', categories=categoriesReceived)

    # ---------------------------------------------------------

    @staticmethod
    def addCategory(db: Collection):
        idCategory = int(get_next_sequence_value(db, "idCategory"))
        name = request.form['name']

        if idCategory:
            category = Category(idCategory, name)
            db.insert_one(category.toDBCollection())
            return redirect(url_for('categories'))
        else:
            return jsonify({'error': 'Categoría no insertada', 'status': '404 Not Found'}), 404

    # ---------------------------------------------------------

    @staticmethod
    def getAllCategories(db: Collection):
        allCategories = db.find()
        categoryList = [
            {
                'idCategory': category.get('idCategory'),
                'name': category.get('name')
            }
            for category in allCategories
        ]
        return jsonify(categoryList), 200

    # ---------------------------------------------------------

    @staticmethod
    def getCategoryById(db: Collection, idCategory: int):
        if idCategory:
            idCategory = int(idCategory)
            matchingCategory = db.find({'idCategory': idCategory})
            if matchingCategory:
                categoryFound = [
                    {
                        'idCategory': category.get('idCategory'),
                        'name': category.get('name')
                    }
                    for category in matchingCategory
                ]
                return jsonify(categoryFound), 200
            else:
                return jsonify({'error': 'Categoría no encontrada', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Falta de datos o método incorrecto', 'status': '400 Bad Request'}), 400

    # ---------------------------------------------------------

    @staticmethod
    def getContentByCategory(categoryCollection: Collection, movieCollection: Collection, seriesCollection: Collection):
        idCategory = int(request.args.get('idCategory'))
        print(idCategory)

        if idCategory:
            matchingCategory = categoryCollection.find({'idCategory': idCategory})
            print(matchingCategory)

            if matchingCategory:
                contentList = []
                matchingMovie = movieCollection.find({'category': {'$in': [str(idCategory)]}})

                contentList.append({'Content': 'Movies'})

                for movie in matchingMovie:
                    contentList.append({
                        'idMovie': movie.get('idMovie'),
                        'title': movie.get('title'),
                        'urlVideo': movie.get('urlVideo'),
                        'urlTitlePage': movie.get('urlTitlePage'),
                        'releaseDate': movie.get('releaseDate'),
                        'synopsis': movie.get('synopsis'),
                        'description': movie.get('description'),
                        'isSuscription': movie.get('isSuscription'),
                        'duration': movie.get('duration'),
                        'languages': movie.get('languages'),
                        'categories': movie.get('categories'),
                        'characters': movie.get('characters'),
                        'participants': movie.get('participants'),
                        'trailer': movie.get('trailer'),
                    })

                contentList.append({'Content': 'Series'})
                matchingSerie = seriesCollection.find({'category': {'$in': [str(idCategory)]}})

                for series in matchingSerie:
                    contentList.append({
                        'idSeries': series.get('idSeries'),
                        'title': series.get('title'),
                        'duration': series.get('duration'),
                        'urlTitlePage': series.get('urlTitlePage'),
                        'releaseDate': series.get('releaseDate'),
                        'synopsis': series.get('synopsis'),
                        'description': series.get('description'),
                        'isSuscription': series.get('isSuscription'),
                        'seasons': series.get('seasons'),
                        'languages': series.get('languages'),
                        'categories': series.get('categories'),
                        'characters': series.get('characters'),
                        'participants': series.get('participants'),
                        'trailer': series.get('trailer')
                    })

                return jsonify(contentList), 200

            else:
                return jsonify({'error': 'Película no encontrada', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Falta de datos o método incorrecto', 'status': '400 Bad Request'}), 400
