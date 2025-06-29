from django import forms
from .models import  ContactMessage
import re

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
