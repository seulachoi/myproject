# mongodb localhost -> ubuntu server data copy (transfer)

'''
from pymongo import MongoClient

def do_sync():
    ## mongoDB
    client_from = MongoClient('mongodb://localhost', 27017)
    db_from = client_from.dbsparta

    coll_names = [collection for collection in db_server.list_collection_names()]

    ## mongoDB
    client_to = MongoClient('mongodb://test:test@내아이피', 27017)
    db_to = client_to.dbsparta

    for coll in coll_names:
        print(coll)
        db_to[coll].drop()

        docs = db_from[coll].find({})
        db_to[coll].insert_many(docs)

if __name__ == "__main__":
    do_sync()
    '''
