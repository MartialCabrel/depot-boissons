from django.contrib import admin
from .models import Facture, LigneFacture

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ('numero', 'client', 'annexe', 'statut', 'date_creation', 'creee_par')
    list_filter = ('statut', 'annexe')
    search_fields = ('numero', 'client__nom')

@admin.register(LigneFacture)
class LigneFactureAdmin(admin.ModelAdmin):
    list_display = ('facture', 'produit', 'quantite', 'prix_unitaire', 'sous_total')