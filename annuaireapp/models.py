
from django.db import models
from datetime import date

class Artisan(models.Model):
    nom = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20, blank=True)
    ville = models.CharField(max_length=100, blank=True)
    profil_complet = models.BooleanField(default=False)
    # Métier : choix parmi la liste + possibilité autre
    METIER_CHOICES = [
        ('Plombier', 'Plombier'),
        ('Électricien', 'Électricien'),
        ('Menuisier', 'Menuisier'),
        ('Maçon', 'Maçon'),
        ('Peintre', 'Peintre'),
        ('autre', 'Autre'),
    ]
    metier = models.CharField(max_length=50, choices=METIER_CHOICES)
    nouveau_metier = models.CharField(max_length=100, blank=True, null=True)

    # Année de début (ex: 2015)
    date_debut_activite = models.IntegerField(blank=True, null=True)

    # Calculée automatiquement à partir de l'année de début
    experience = models.IntegerField(blank=True, null=True)

    description = models.TextField(blank=True)
    photos = models.ImageField(upload_to='artisans_photos/', blank=True, null=True)

    def calculer_experience(self):
        """Retourne le nombre d'années d'expérience à partir de l'année de début."""
        if self.date_debut_activite:
            annee_actuelle = date.today().year
            return max(0, annee_actuelle - self.date_debut_activite)
        return None

    def save(self, *args, **kwargs):
        self.experience = self.calculer_experience()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

def save(self, *args, **kwargs):
    self.experience = self.calculer_experience()
    super().save(*args, **kwargs)



class ContactMessage(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} - {self.email}"
