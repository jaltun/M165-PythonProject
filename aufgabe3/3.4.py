from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

connection_string = "mongodb+srv://juliaaltun:12345@cluster0.h8ibzgi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(connection_string)
db = client.db_restaurant
collection = db.restaurants
print(collection)


#3.4 Search restaurant
name = input("Enter a restaurant name (leave blank to ignore): ")
cuisine = input("Enter a cuisine (leave blank to ignore): ")

# Build the query
query = {}
if name:
    query["name"] = {"$regex": name, "$options": "i"}
if cuisine:
    query["cuisine"] = {"$regex": cuisine, "$options": "i"}

results = collection.find(query)

for result in results:
    print(f"Restaurant: {result['name']}, Cuisine: {result['cuisine']}")