from django.contrib import admin
from .models import Tournee, LigneTournee, Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'telephone', 'type_client', 'date_creation')
    list_filter = ('type_client',)
    search_fields = ('nom',)

@admin.register(Tournee)
class TourneeAdmin(admin.ModelAdmin):
    list_display = ('livreur', 'annexe', 'date', 'statut')
    list_filter = ('statut', 'annexe')

@admin.register(LigneTournee)
class LigneTourneeAdmin(admin.ModelAdmin):
    list_display = ('tournee', 'produit', 'quantite_chargee', 'quantite_vendue', 'quantite_retournee')