from django.contrib import admin
from .models import  ContactMessage, Artisan

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'date_envoi')
    search_fields = ('nom', 'email', 'message')
    readonly_fields = ('nom', 'email', 'message', 'date_envoi')
    ordering = ('-date_envoi',)

@admin.register(Artisan)
class ArtisanAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'metier', 'ville', 'experience')
    search_fields = ('nom', 'email', 'ville', 'metier', 'nouveau_metier')
    list_filter = ('metier', 'ville')
    readonly_fields = ('experience',)
    ordering = ('nom',)