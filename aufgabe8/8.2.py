from pymongo import MongoClient
from PIL import Image, ImageDraw

mongo_client = MongoClient('localhost', 27017)
database = mongo_client['db_restaurants']
neighborhood_collection = database['neighborhoods']

def fetch_coordinates():
    # Hole das erste Dokument aus der Sammlung
    neighborhood = neighborhood_collection.find_one()
    # Prüfe, ob das Dokument und das 'geometry'-Feld existieren
    if neighborhood and 'geometry' in neighborhood:
        # Hole 'coordinates' aus dem 'geometry'-Feld, leere Liste als Fallback
        coordinates = neighborhood['geometry'].get('coordinates', [])
        # Wenn Koordinaten vorhanden, gib die ersten zurück
        if coordinates:
            return coordinates[0]
    # Falls keine Koordinaten gefunden, zeige eine Nachricht
    print("Polygonkoordinaten nicht gefunden.")
    # Gib eine leere Liste zurück, falls keine Koordinaten gefunden wurden
    return []

def create_image_with_polygon(coords):
    if not coords:
        print("Keine Koordinaten zum Zeichnen verfügbar.")
        return

    # Erstelle ein neues leeres Bild
    image = Image.new("RGB", (3000, 3000), "white")
    draw = ImageDraw.Draw(image)

    # Extrahiere X- und Y-Werte aus den Koordinaten
    x_values = [point[0] for point in coords]
    y_values = [point[1] for point in coords]
    # Finde die minimalen und maximalen X-Werte
    min_x, max_x = min(x_values), max(x_values)
    # Finde die minimalen und maximalen Y-Werte
    min_y, max_y = min(y_values), max(y_values)

    # Funktion, um Koordinaten an die Bildgröße anzupassen, mit einem Rand
    def scale_coordinate(coord, min_coord, max_coord, size):
        return int((coord - min_coord) / (max_coord - min_coord) * (size - 1000) + 500)

    scaled_coords = [(scale_coordinate(x, min_x, max_x, image.size[0]),
                      scale_coordinate(y, min_y, max_y, image.size[1])) for x, y in coords]

    # Zeichne das Polygon
    draw.polygon(scaled_coords, outline="black", fill="blue")

    # Zeige das Bild an
    image.show()

# Hole Koordinaten und zeichne das Polygon
polygon_coordinates = fetch_coordinates()
create_image_with_polygon(polygon_coordinates)