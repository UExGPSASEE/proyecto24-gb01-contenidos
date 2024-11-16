from pymongo import MongoClient

def conexionMongoDB():
    try:
        client=MongoClient('localhost',27017)
        database=client['MedifliContent']
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    return database


db = conexionMongoDB()
counter_collection = db['counters']
def get_next_id(counter_name):
    counter = counter_collection.find_one_and_update(
        {'_id': counter_name},
        {'$inc': {'sequence_value': 1}},
        upsert=True,  # Crear el contador si no existe
        return_document=True
    )
    return counter['sequence_value']
