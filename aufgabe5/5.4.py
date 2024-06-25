import matplotlib.pyplot as plt
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client.system_usage
collection = db.usage_data

# Alle Dokumente aus der Datenbank abrufen
logs = collection.find()

# Listen für die Daten erstellen
timestamps = []
cpu_usages = []
ram_usages = []

# Daten aus den Dokumenten in die Listen einfügen
for log in logs:
    timestamps.append(log['timestamp'])
    cpu_usages.append(log['cpu'])
    ram_usages.append(log['ram_used'] / log['ram_total'])

# Daten in einem Graphen darstellen
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(timestamps, cpu_usages, label='CPU usage')
plt.title('System Usage Over Time')
plt.ylabel('CPU usage (%)')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(timestamps, ram_usages, label='RAM usage')
plt.xlabel('Time')
plt.ylabel('RAM usage (%)')
plt.legend()

plt.tight_layout()
plt.show()