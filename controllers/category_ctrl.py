from flask import render_template, request, jsonify, redirect, url_for
from database import get_next_sequence_value as get_next_sequence_value
from pymongo.collection import Collection
from models.category import Category

class CategoryCtrl:

    @staticmethod
    def render_template(db: Collection):
        categoriesReceived = db.find()
        return render_template('Category.html', categories=categoriesReceived)
# ---------------------------------------------------------

    @staticmethod
    def addCategory(db: Collection):
        idCategory = get_next_sequence_value(db,"idCategory")
        name = request.form['name']

        if idCategory:
            category = Category(idCategory, name)
            db.insert_one(category.toDBCollection())
            return redirect(url_for('categories'))
        else:
            return jsonify({'error': 'Category not found or not added', 'status':'404 Not Found'}), 404

# ---------------------------------------------------------

    @staticmethod
    def getAllCategories(db: Collection):
        allCategories = db.find()
        category_list = [
            {
                'idCategory' : category.get('idCategory'),
                'name' : category.get('name')
            }
            for category in allCategories
        ]
        return jsonify(category_list), 200

# ---------------------------------------------------------

    @staticmethod
    def getCategoryById(db: Collection):
        idCategory = int(request.args.get('idCategory'))
        if idCategory:
            matching_category = db.find({'idCategory': idCategory})
            if matching_category:
                categoryFound = [
                {
                    'idCategory' : category.get('idCategory'),
                    'name' : category.get('name')
                }
                for category in matching_category
                ]
                return jsonify(categoryFound), 200
            else:
                return jsonify({'error': 'Category not found', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400