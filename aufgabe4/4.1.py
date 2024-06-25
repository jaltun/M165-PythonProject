import os

path = os.getenv('PATH')

# Liest die Umgebungsvariable 'PATH', teilt sie an Pfadtrennzeichen und gibt jeden Pfad einzeln aus.
directories = path.split(os.pathsep)

# Schleife
for directory in directories:
    print("-  " + directory)
