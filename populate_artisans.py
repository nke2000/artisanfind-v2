import os
import django
import random
import string
import time
from urllib.request import urlopen
from django.core.files.temp import NamedTemporaryFile

# 1. Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monannuaire.settings')
django.setup()

from annuaireapp.models import Artisan

# 2. Données possibles
METIERS_CHOICES = [
    "Plombier", "Électricien", "Menuisier", "Maçon", "Peintre",
    "Chauffagiste", "Serrurier", "Carreleur", "Couvreur", "Jardinier"
]

LOCALISATIONS = ["Abidjan", "Yamoussoukro", "Bouaké", "Daloa", "San Pedro"]

DESCRIPTIONS = [
    "Professionnel expérimenté et fiable.",
    "Spécialiste reconnu dans son domaine.",
    "Travail de qualité garanti.",
    "Disponible et à l’écoute.",
    "Service rapide et efficace."
]

# 3. Générateur d'artisan
def create_artisan(index):
    nom = ''.join(random.choices(string.ascii_letters, k=7)).capitalize()
    # Ajout d'un suffixe pour garantir unicité email
    email = f"{nom.lower()}{index}@gmail.com"
    telephone = f"07{random.randint(10000000, 99999999)}"
    metier = random.choice(METIERS_CHOICES)
    localisation = random.choice(LOCALISATIONS)
    experience = random.randint(1, 30)
    description = random.choice(DESCRIPTIONS)

    # Téléchargement de l’image depuis Unsplash avec un paramètre aléatoire
    image_url = f"https://source.unsplash.com/400x400/?{metier.lower()}&sig={index}"
    img_temp = NamedTemporaryFile(suffix=".jpg")
    img_temp.write(urlopen(image_url).read())
    img_temp.flush()

    artisan = Artisan(
        nom=nom,
        email=email,
        telephone=telephone,
        metier=metier,
        localisation=localisation,
        experience=experience,
        description=description,
    )
    artisan.photos.save(f"{nom.lower()}_{index}.jpg", img_temp)
    artisan.save()

# 4. Boucle de création
if __name__ == '__main__':
    for i in range(1, 101):  # 100 artisans
        try:
            create_artisan(i)
            print(f"{i}/100 artisan ajouté avec photo")
            time.sleep(0.5)  # pause pour éviter surcharge serveur images
        except Exception as e:
            print(f"⚠️ Erreur à l’artisan {i} : {e}")
