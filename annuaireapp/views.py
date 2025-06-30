from django.shortcuts import render, redirect
from .models import Artisan
from .forms import  ContactForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from collections import defaultdict
from django.db.models import Q
import unicodedata

def detail_artisan_modal(request, artisan_id):
    artisan = get_object_or_404(Artisan, id=artisan_id)
    html = render_to_string('annuaireapp/detail_artisan_modal.html', {'artisan': artisan})
    return JsonResponse({'html': html})
# Page d'accueil
def index(request):
    ville = request.GET.get('ville', '').strip()
    metier = request.GET.get('metier', '').strip()
    nouveau_metier = request.GET.get('nouveau_metier', '').strip()
    keyword = request.GET.get('keyword', '').strip()

    ville_norm = normalize(ville)
    metier_norm = normalize(nouveau_metier if metier == 'autre' else metier)
    keyword_norm = normalize(keyword)

    artisans = Artisan.objects.filter(profil_complet=True)

    if not (ville or metier or keyword):
        artisans = artisans[:15]
    else:
        filtered_artisans = []
        for artisan in artisans:
            ville_artisan = normalize(artisan.ville)
            metier_artisan = normalize(
                artisan.nouveau_metier if artisan.metier == 'autre' and artisan.nouveau_metier else artisan.metier
            )
            nom_artisan = normalize(artisan.nom)
            description_artisan = normalize(artisan.description or "")

            if (
                (not ville or ville_norm in ville_artisan) and
                (not metier or metier_norm in metier_artisan) and
                (not keyword or (keyword_norm in nom_artisan or keyword_norm in description_artisan))
            ):
                filtered_artisans.append(artisan)

        artisans = filtered_artisans

    context = {
        'artisans': artisans,
        'metier_choices': Artisan.METIER_CHOICES,
        'ville': ville,
        'metier': metier,
        'nouveau_metier': nouveau_metier,
        'keyword': keyword,
    }

    return render(request, 'annuaireapp/index.html', context)



def inscription_artisan(request):
    return render(request, 'annuaireapp/inscription_artisan.html')
# À propos
def a_propos(request):
    return render(request, 'annuaireapp/a-propos.html')

def connexion(request):
    return render(request, 'annuaireapp/connexion.html')

def inscription_preliminaire(request):
    return render(request, 'annuaireapp/inscription_preliminaire.html')

def metiers(request):
    return render(request, 'annuaireapp/metiers.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'annuaireapp/contact.html', {
                'form': ContactForm(),
                'success': True
            })
    else:
        form = ContactForm()
    return render(request, 'annuaireapp/contact.html', {'form': form})


def inscription_preliminaire(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'annuaireapp/inscription_preliminaire.html')

        if Artisan.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return render(request, 'annuaireapp/inscription_preliminaire.html')

        hashed_password = make_password(password)
        artisan = Artisan.objects.create(email=email, password=hashed_password)

        request.session['artisan_email'] = email
        messages.success(request, "Inscription réussie. Complétez votre profil.")
        return redirect('inscription_artisan')

    return render(request, 'annuaireapp/inscription_preliminaire.html')


def connexion(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            artisan = Artisan.objects.get(email=email)
            if check_password(password, artisan.password):
                request.session['artisan_email'] = artisan.email
                messages.success(request, "Connexion réussie.")
                return redirect('inscription_artisan')
            else:
                messages.error(request, "Mot de passe incorrect.")
        except Artisan.DoesNotExist:
            messages.error(request, "Email non reconnu.")

    return render(request, 'annuaireapp/connexion.html')



def inscription_artisan(request):
    artisan = None
    email = request.session.get('artisan_email', '')

    if email:
        try:
            artisan = Artisan.objects.get(email=email)
        except Artisan.DoesNotExist:
            artisan = None

    if request.method == 'POST':
        nom = request.POST.get('nom')
        telephone = request.POST.get('telephone')
        ville = request.POST.get('ville')
        metier = request.POST.get('metier')
        nouveau_metier = request.POST.get('nouveau_metier') if metier == 'autre' else ''
        date_debut_str = request.POST.get('annee_debut_activite')
        description = request.POST.get('description')
        photo = request.FILES.get('photos')

        try:
            date_debut = int(date_debut_str) if date_debut_str else None
        except ValueError:
            date_debut = None

        if artisan:
            artisan.nom = nom
            artisan.telephone = telephone
            artisan.ville = ville
            artisan.metier = metier
            artisan.nouveau_metier = nouveau_metier
            artisan.date_debut_activite = date_debut
            artisan.description = description
            artisan.photos = photo or artisan.photos
            artisan.profil_complet = True
            artisan.save()


            messages.success(request, "Profil complété avec succès.")
            return redirect('index')
        else:
            messages.error(request, "Aucun compte associé à cet email.")

    context = {
        'email': email,
        'artisan': artisan,
        'metier_choices': Artisan.METIER_CHOICES,
    }
    return render(request, 'annuaireapp/inscription_artisan.html', context)


def deconnexion(request):
    request.session.flush()
    messages.success(request, "Vous avez été déconnecté.")
    return redirect('index')




def metiers(request):
    metiers_dict = defaultdict(list)

    for artisan in Artisan.objects.all():
        nom_metier = artisan.metier
        if nom_metier == 'autre' and artisan.nouveau_metier:
            nom_metier = artisan.nouveau_metier
        metiers_dict[nom_metier].append(artisan)

    # Structure attendue dans le template
    metiers_data = [{'nom': nom, 'artisans': artisans} for nom, artisans in metiers_dict.items()]

    return render(request, 'annuaireapp/metiers.html', {
        'metiers_data': metiers_data
    })


def normalize(text):
    """
    Supprime les accents et convertit le texte en minuscule.
    """
    if not text:
        return ''
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    ).lower()