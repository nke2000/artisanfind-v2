import os
import django
import random
from faker import Faker
from urllib.request import urlopen
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monannuaire.settings')
django.setup()

from annuaireapp.models import Artisan

fake = Faker('fr_FR')

metiers = [metier[0] for metier in Artisan.METIERS_CHOICES]

def create_artisan():
    nom = fake.name()
    email = fake.unique.email()
    telephone = f"07{random.randint(10000000, 99999999)}"
    localisation = fake.city()
    metier = random.choice(metiers)
    experience = random.randint(1, 30)
    description = fake.text(max_nb_chars=200)

    # Télécharger une image d’artisan simulée
    image_url = f"https://loremflickr.com/400/400/worker,artisan?random={random.randint(1,10000)}"
    img_temp = NamedTemporaryFile(delete=True, suffix=".jpg")
    img_temp.write(urlopen(image_url).read())
    img_temp.flush()

    artisan = Artisan(
        nom=nom,
        email=email,
        telephone=telephone,
        localisation=localisation,
        metier=metier,
        experience=experience,
        description=description,
    )
    artisan.photos.save(f"{nom.replace(' ', '_')}.jpg", File(img_temp))
    artisan.save()

if __name__ == '__main__':
    for i in range(50):
        create_artisan()
        print(f"{i+1}/50 artisan ajouté avec photo")
