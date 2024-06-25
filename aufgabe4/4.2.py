from pymongo import MongoClient
import os

connection_string = os.getenv('MONGO_CONNECTION_STRING')

print ("Connection String: ", connection_string)
client = MongoClient(connection_string)

print("Databases:")
for db in client.list_database_names():
    print(db)