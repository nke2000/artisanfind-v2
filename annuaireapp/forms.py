from django import forms
from .models import Artisan
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class ArtisanForm(forms.ModelForm):
    mot_de_passe = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'placeholder': 'Entrez un mot de passe sécurisé'}),
        min_length=6,
        max_length=128
    )

    confirmation = forms.CharField(
        label="Confirmation du mot de passe",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmez le mot de passe'})
    )

    class Meta:
        model = Artisan
        exclude = ['date_inscription']

    def clean(self):
        cleaned_data = super().clean()
        mot_de_passe = cleaned_data.get("mot_de_passe")
        confirmation = cleaned_data.get("confirmation")
        if mot_de_passe != confirmation:
            raise ValidationError(_("Les mots de passe ne correspondent pas."))
        return cleaned_data

    def clean_telephone(self):
        numero = self.cleaned_data.get('telephone')
        if not re.match(r'^\d{10}$', numero):
            raise forms.ValidationError("Le numéro doit contenir exactement 10 chiffres.")
        return numero

    def save(self, commit=True):
        artisan = super().save(commit=False)
        # (optionnel) hachage si tu veux sécuriser
        artisan.mot_de_passe = self.cleaned_data['mot_de_passe']
        if commit:
            artisan.save()
        return artisan



from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['nom', 'email', 'message']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Votre nom'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'exemple@mail.com'
            }),
            'message': forms.Textarea(attrs={
                'rows': 5,
                'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Votre message'
            }),
        }


from django import forms
from .models import Artisan

class ArtisanForm(forms.ModelForm):
    class Meta:
        model = Artisan
        fields = ['nom', 'telephone', 'ville', 'localisation', 'metier', 'experience', 'description', 'photos']
