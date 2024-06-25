from room import Room
from dao_room import Dao_room

dao_room = Dao_room("mongodb+srv://juliaaltun:12345@cluster0.h8ibzgi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Create
#room_create = Room("Pilatus", 12, True)
#dao_room.create(room_create)

# Read
#room_read = dao_room.read()

# Update
#room_update = Room("Pilatus", 13, False)
#updates = {"size": room_update.size, "available": room_update.available}
#dao_room.update(room_update.name, updates)

# Delete
# Assuming the ID of the room you want to delete is known
room_id_to_delete = "6662e1063413afd5b2f66c81"

# Delete
dao_room.delete_by_id(room_id_to_delete)