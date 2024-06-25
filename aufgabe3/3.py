from pymongo import MongoClient

connection_string = "mongodb://localhost:27017/"
client = MongoClient(connection_string)
db = client.db_restaurants
collection = db.restaurants

# Stadtbezirke 3.1

boroughs = collection.distinct('borough')

print("Stadtbezirke :" + "\n")

for borough in boroughs:
    print("- " + borough)

print("\n" + "--------------------------" + "\n")

# Top 3 high Score 3.2

print("Top 3 Restaurants:" + "\n")

bestScoredRestaurants = [
    {"$unwind": "$grades"},
    {"$group": {
        "_id": "$name",
        "averageScore": {"$avg": "$grades.score"}
    }},
    {"$sort": {"averageScore": -1}},
    {"$limit": 3}
]

# führt die Aggregationspipeline auf der MongoDB-Sammlung `collection` aus und speichert die Ergebnisse in `results`
results = collection.aggregate(bestScoredRestaurants)

for i, result in enumerate(results, start=1):
    print(f"Platz {i}: {result['_id']}, Average Score: {result['averageScore']}")

print("\n" + "--------------------------" + "\n")

# Restaurant nähe Le Perdigord 3.3

print("Nächstes Restaurant :" + "\n")

collection.create_index([("address.coord", "2dsphere")])

# Find the coordinates
le_perigord = collection.find_one({"name": "Le Perigord"})
if not le_perigord:
    print("Restaurant 'Le Perigord' not found.")
else:
    le_perigord_coords = le_perigord["address"]["coord"]

    # Define the aggregation pipeline
    pipeline = [
        {
            # Nutzt `$geoNear` zum Finden des nächstgelegenen Dokuments basierend auf Koordinaten, mit Berücksichtigung der Erdkrümmung.
            "$geoNear": {
                "near": le_perigord_coords,
                "distanceField": "distance",
                "spherical": True
            }
        },
        {
            # Filtert das Dokument mit dem gleichen `_id` wie `le_perigord` heraus
            "$match": {
                "_id": {"$ne": le_perigord["_id"]}
            }
        },
        {
            "$limit": 1
        }
    ]

    results = collection.aggregate(pipeline)

    for result in results:
        print(f"- {result['name']}, Distance: {result['distance']}")