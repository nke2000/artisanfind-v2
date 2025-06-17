from django.contrib import admin
from .models import Artisan, ContactMessage

@admin.register(Artisan)
class ArtisanAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'telephone', 'ville', 'metier', 'experience')
    list_filter = ('metier', 'ville')
    search_fields = ('nom', 'email', 'ville', 'metier')
    readonly_fields = ('mot_de_passe',)  # Pour éviter la modification directe
    fieldsets = (
        ("Informations personnelles", {
            'fields': ('nom', 'email', 'telephone', 'ville', 'mot_de_passe')
        }),
        ("Détails professionnels", {
            'fields': ('metier', 'experience', 'description', 'photos')
        }),
        ("Localisation", {
            'fields': ('localisation',)
        }),
    )

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'date_envoi')
    search_fields = ('nom', 'email', 'message')
    readonly_fields = ('nom', 'email', 'message', 'date_envoi')
    ordering = ('-date_envoi',)
