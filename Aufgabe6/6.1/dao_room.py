from pymongo import MongoClient
from room import Room

class Dao_room():
    def __init__(self, connection_string):
        # Initialisiert eine Instanz der Klasse Dao_room
        self.connection_string = connection_string
        # Erstellt eine Verbindung zur MongoDB und wählt die Sammlung "rooms" in der Datenbank "buildings"
        self.col = MongoClient(connection_string)["buildings"]["rooms"]

    def create(self, room):
        # Fügt einen neuen Raum in die Sammlung ein
        self.col.insert_one(room.__dict__)

    def read(self):
        # Liest einen Raum aus der Sammlung und erstellt eine Room-Instanz daraus
        room = Room(**self.col.find_one())
        return room

    def update(self, room):
        # Aktualisiert einen Raum in der Sammlung basierend auf der ID
        self.col.update_one({"_id": room._id}, {"$set": room.__dict__})

    def delete(self, room_id):
        # Löscht einen Raum aus der Sammlung basierend auf der ID
        self.col.delete_one({"_id": room_id})
