from django.contrib import admin
from .models import Categorie, Produit, StockAnnexe

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom',)

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'prix_vente', 'unite', 'actif')
    list_filter = ('categorie', 'actif')
    search_fields = ('nom',)

@admin.register(StockAnnexe)
class StockAnnexeAdmin(admin.ModelAdmin):
    list_display = ('produit', 'annexe', 'quantite', 'seuil_alerte')
    list_filter = ('annexe',)