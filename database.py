from pymongo import MongoClient

def conexionMongoDB():
    try:
        client=MongoClient('localhost',27017)
        database=client['movies']
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    return database