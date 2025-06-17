# models.py
from django.db import models

class Artisan(models.Model):
    METIERS_CHOICES = [
        ("Plombier", "Plombier"),
        ("Électricien", "Électricien"),
        ("Menuisier", "Menuisier"),
        ("Maçon", "Maçon"),
        ("Peintre", "Peintre"),
    ]

    nom = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=10)
    ville = models.CharField(max_length=100)
    localisation = models.CharField(max_length=100, blank=True)
    metier = models.CharField(max_length=50, choices=METIERS_CHOICES)
    experience = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    photos = models.ImageField(upload_to='artisan_photos/', blank=True, null=True)
    mot_de_passe = models.CharField(max_length=255)  # à hasher !

    def __str__(self):
        return f"{self.nom} - {self.metier}"



class ContactMessage(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} - {self.email}"
