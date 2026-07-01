from django.contrib import admin
from .models import Paiement, SessionCaisse

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('facture', 'montant', 'mode_paiement', 'date', 'encaisse_par')
    list_filter = ('mode_paiement',)

@admin.register(SessionCaisse)
class SessionCaisseAdmin(admin.ModelAdmin):
    list_display = ('caissiere', 'annexe', 'date_ouverture', 'statut', 'montant_ouverture')
    list_filter = ('statut', 'annexe')