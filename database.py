from pymongo import MongoClient
from pymongo.collection import Collection


def conexionMongoDB():
    try:
        client = MongoClient('localhost', 27017)
        database = client['MedifliContent']
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    return database


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
