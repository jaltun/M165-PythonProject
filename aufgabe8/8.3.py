from PIL import Image, ImageDraw
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['db_restaurants']
neighborhoods = db['neighborhoods']

polygons = neighborhoods.find()

im = Image.new(mode="RGB", size=(4000, 4000), color="white")
draw = ImageDraw.Draw(im)

# Sammle alle Koordinaten aus den Polygonen
all_coordinates = []
for polygon_document in polygons:
    geometry_type = polygon_document['geometry']['type']
    coordinates = polygon_document['geometry']['coordinates']

    # Verarbeite Polygone und MultiPolygone unterschiedlich
    if geometry_type == "Polygon":
        for coordinate in coordinates[0]:
            all_coordinates.append(coordinate)
    elif geometry_type == "MultiPolygon":
        for polygon in coordinates:
            for coordinate in polygon[0]:
                all_coordinates.append(coordinate)

# Berechne minimale und maximale Koordinaten für Skalierung
min_x = min(all_coordinates, key=lambda x: x[0])[0]
max_x = max(all_coordinates, key=lambda x: x[0])[0]
min_y = min(all_coordinates, key=lambda x: x[1])[1]
max_y = max(all_coordinates, key=lambda x: x[1])[1]

# Berechne Skalierung und Verschiebung für die Darstellung
width, height = im.size
scale = min(width / (max_x - min_x), height / (max_y - min_y))
offset_x = -min_x
offset_y = -min_y

# Berechne das Zentrum des Bildes für eventuelle Rotationen
center_x = width / 2
center_y = height / 2

fill_color = "green"

# Zeichne Polygone mit umgekehrter Y-Achse
for polygon_document in polygons.rewind():
    geometry_type = polygon_document['geometry']['type']
    coordinates = polygon_document['geometry']['coordinates']

    if geometry_type == "Polygon":
        # Skaliere und verschiebe Koordinaten, Y-Achse umkehren
        scaled_polygon = [(scale * (x + offset_x),
                           (scale * (y + offset_y) - center_y) * -1 + center_y)
                          for x, y in coordinates[0]]
        draw.polygon(scaled_polygon, outline="black", fill=fill_color)
    elif geometry_type == "MultiPolygon":
        for polygon in coordinates:
            scaled_polygon = [(scale * (x + offset_x),
                               (scale * (y + offset_y) - center_y) * -1 + center_y)
                              for x, y in polygon[0]]
            draw.polygon(scaled_polygon, outline="black", fill=fill_color)

im.show()