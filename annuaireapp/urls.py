from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('a-propos/', views.a_propos, name="a_propos"),
    path('contact/', views.contact, name="contact"),
    path('artisans/', views.artisans, name="artisans"),
    path('metiers/', views.metiers, name="metiers"),
    path('api/artisans/<str:metier_nom>/', views.artisans_json_par_metier, name="artisans_json_par_metier"),
    path('pre-inscription/', views.pre_inscription, name="pre_inscription"),
    path('inscription-artisan/', views.inscription_artisan, name="inscription_artisan"),
    path('connexion/', views.connexion, name="connexion"),  # ✅ Correction ici
    path('deconnexion/', views.deconnexion, name="deconnexion"),
]
