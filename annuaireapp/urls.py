from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name="index"),
    path('metiers/', views.metiers, name="metiers"),
    path('a-propos/', views.a_propos, name="a_propos"),
    path('contact/', views.contact, name="contact"),
    path('inscription-preliminaire/', views.inscription_preliminaire, name="inscription_preliminaire"),
    path('connexion/', views.connexion, name="connexion"),
    path('inscription-artisan/', views.inscription_artisan, name="inscription_artisan"),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('artisan/<int:artisan_id>/modal/', views.detail_artisan_modal, name='detail_artisan_modal'),

]
