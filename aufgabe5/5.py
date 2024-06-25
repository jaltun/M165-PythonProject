import time
from pymongo import MongoClient
import psutil
from datetime import datetime

class Power:
    def __init__(self, timestamp=None):
        self.cpu = psutil.cpu_percent()
        self.ram_total = psutil.virtual_memory().total
        self.ram_used = psutil.virtual_memory().used
        self.timestamp = datetime.now() if timestamp is None else timestamp

client = MongoClient("mongodb+srv://juliaaltun:12345@cluster0.h8ibzgi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.system_usage
collection = db.usage_data

while True:
    power = Power()

    # Daten in Datenbank speichern
    collection.insert_one(power.__dict__)

    # Logs speicherung
    if collection.count_documents({}) > 10000:
        oldest_logs = collection.find().sort("timestamp", 1).limit(collection.count_documents({}) - 10000)
        for log in oldest_logs:
            collection.delete_one({"_id": log["_id"]})

    time.sleep(1)