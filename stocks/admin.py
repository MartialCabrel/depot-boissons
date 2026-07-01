from django.contrib import admin
from .models import MouvementStock, Transfert

@admin.register(MouvementStock)
class MouvementStockAdmin(admin.ModelAdmin):
    list_display = ('produit', 'annexe', 'type_mouvement', 'quantite', 'date', 'effectue_par')
    list_filter = ('type_mouvement', 'annexe')
    search_fields = ('produit__nom',)

@admin.register(Transfert)
class TransfertAdmin(admin.ModelAdmin):
    list_display = ('produit', 'annexe_source', 'annexe_destination', 'quantite', 'date')