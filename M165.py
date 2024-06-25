from pymongo import MongoClient
import bson

connection_string = "mongodb+srv://juliaaltun:12345@cluster0.h8ibzgi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(connection_string)

print(client.server_info())

dblist = client.list_database_names()

while True:
    for db in dblist:
        print(db)

    db=None

    while db is None:
        sel = input("Select Database: ")
        if sel not in client.list_database_names():
            print(f"Database {sel} does not exists.")
            continue
        db = client[sel]

    collist = db.list_collection_names()

    if not collist:
        input("No Collections. Press any button to return:")
        continue

    for col in collist:
        print(col)

    sel = input("Select a Collection: ")
    if sel not in db.list_collection_names():
       print(f"Collection {sel} does not exists.")
       continue
    col = db[sel]

    doclist = col.find({})

    doclist = [doc for doc in doclist]

    if not doclist:
        input("No Documents. Press any button to return:")
        continue

    doc = db[sel].find({}, {"_id"})
    print("Documents:")
    for document in doc:
        print(document["_id"])

    sel = input("Select a Document: ")
    id = bson.ObjectId(sel)
    query = { "_id": id }

    document = col.find_one(query)

    for key, value in document.items():
        print(f"{key}: {value}")

    input("Press any button to return")
