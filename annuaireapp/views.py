from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import ArtisanForm
from .models import Artisan
import json
import hashlib
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password

# Page d'accueil
def index(request):
    artisans = Artisan.objects.all()
    return render(request, 'annuaireapp/index.html', {'artisans': artisans})

# À propos
def a_propos(request):
    return render(request, 'annuaireapp/a-propos.html')

# Contact
def contact(request):
    return render(request, 'annuaireapp/contact.html')

# Liste des artisans
def artisans(request):
    artisans = Artisan.objects.all()
    return render(request, 'annuaireapp/artisans.html', {'artisans': artisans})

# Vue JSON : artisans par métier (utilisée en AJAX)
def artisans_json_par_metier(request, metier_nom):
    artisans = Artisan.objects.filter(metier__iexact=metier_nom)
    data = []
    for artisan in artisans:
        data.append({
            'nom': artisan.nom,
            'email': artisan.email,
            'telephone': artisan.telephone,
            'description': artisan.description,
            'photo_url': artisan.photos.url if artisan.photos else '',
        })
    return JsonResponse({'artisans': data})

# Vue des métiers (affichage par métier)
def metiers(request):
    artisans = Artisan.objects.all()
    metiers = artisans.values_list('metier', flat=True).distinct()

    metiers_data = []
    for metier in metiers:
        artisans_du_metier = artisans.filter(metier=metier)
        metiers_data.append({
            'nom': metier,
            'artisans': artisans_du_metier
        })

    return render(request, 'annuaireapp/metiers.html', {
        'metiers_data': metiers_data
    })

# API de pré-inscription (enregistre email et mot de passe temporairement en session)
@csrf_exempt
def pre_inscription(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            mot_de_passe = data.get("password")

            if not email or not mot_de_passe:
                return JsonResponse({"erreur": "Email ou mot de passe manquant."}, status=400)

            if Artisan.objects.filter(email=email).exists():
                return JsonResponse({"erreur": "Cet email est déjà utilisé."}, status=400)

            request.session['preinscription_email'] = email
            request.session['preinscription_mot_de_passe'] = mot_de_passe

            return JsonResponse({"message": "OK"})
        except Exception:
            return JsonResponse({"erreur": "Données invalides."}, status=400)

    return JsonResponse({"erreur": "Méthode non autorisée."}, status=405)

# Inscription artisan (formulaire complet)
def inscription_artisan(request):
    email = request.session.get('preinscription_email')
    mot_de_passe = request.session.get('preinscription_mot_de_passe')

    if not email or not mot_de_passe:
        return redirect('index')

    if request.method == 'POST':
        form = ArtisanForm(request.POST, request.FILES)
        if form.is_valid():
            artisan = form.save(commit=False)
            artisan.email = email
            artisan.mot_de_passe = hashlib.sha256(mot_de_passe.encode()).hexdigest()
            artisan.save()

            request.session['artisan_id'] = artisan.id
            del request.session['preinscription_email']
            del request.session['preinscription_mot_de_passe']

            return redirect('index')
    else:
        form = ArtisanForm()

    return render(request, 'annuaireapp/inscription_artisan.html', {'form': form, 'email': email})


def deconnexion(request):
    request.session.flush()  # Supprime toutes les données de session
    return redirect('index')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from django.contrib.auth import authenticate, login
def connexion(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            artisan = Artisan.objects.get(email=email)
            if password == artisan.mot_de_passe:  # comparaison directe
                request.session["preinscription_email"] = artisan.email
                return redirect("index")
            else:
                message = "Mot de passe incorrect."
        except Artisan.DoesNotExist:
            message = "Aucun compte trouvé avec cet email."

        return render(request, "annuaireapp/connexion.html", {"message": message})

    return render(request, "annuaireapp/connexion.html")




from django.shortcuts import render, redirect
from .forms import ContactForm
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'annuaireapp/contact.html', {
                'form': ContactForm(),  # Réinitialise le formulaire après succès
                'success': True
            })
    else:
        form = ContactForm()
    return render(request, 'annuaireapp/contact.html', {'form': form})



from django.db import IntegrityError

def inscription_artisan(request):
    # Vérifie que l'utilisateur est "connecté" via la session
    email = request.session.get('preinscription_email')
    mot_de_passe = request.session.get('preinscription_mot_de_passe')

    if not email or not mot_de_passe:
        messages.error(request, "Vous devez être connecté pour vous inscrire.")
        return redirect('connexion')

    if request.method == 'POST':
        form = ArtisanForm(request.POST, request.FILES)
        if form.is_valid():
            # Vérifie si l'email est déjà pris avant de sauvegarder
            if Artisan.objects.filter(email=email).exists():
                messages.error(request, "Cet email est déjà utilisé.")
                return render(request, 'annuaireapp/inscription_artisan.html', {
                    'form': form,
                    'email': email,
                })

            artisan = form.save(commit=False)
            artisan.email = email
            artisan.mot_de_passe = make_password(mot_de_passe)

            localisation_str = form.cleaned_data.get('localisation')
            if localisation_str:
                try:
                    lat_str, lng_str = localisation_str.split(',')
                    artisan.latitude = float(lat_str.strip())
                    artisan.longitude = float(lng_str.strip())
                except Exception:
                    artisan.latitude = None
                    artisan.longitude = None
            else:
                artisan.latitude = None
                artisan.longitude = None

            try:
                artisan.save()
            except IntegrityError:
                messages.error(request, "Erreur lors de l'enregistrement. Cet email est peut-être déjà utilisé.")
                return render(request, 'annuaireapp/inscription_artisan.html', {
                    'form': form,
                    'email': email,
                })

            del request.session['preinscription_email']
            del request.session['preinscription_mot_de_passe']
            request.session['artisan_id'] = artisan.id

            messages.success(request, "Inscription réussie ! Bienvenue.")
            return redirect('index')
        else:
            messages.error(request, "Le formulaire contient des erreurs. Veuillez corriger.")
    else:
        form = ArtisanForm()

    return render(request, 'annuaireapp/inscription_artisan.html', {
        'form': form,
        'email': email,
    })

 
