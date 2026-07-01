from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from django.db import models as django_models
from produits.models import Produit, StockAnnexe
from stocks.models import MouvementStock
from facturation.models import Facture
from caisse.models import Paiement


@login_required
def dashboard(request):
    aujourd_hui = timezone.now().date()

    total_produits = Produit.objects.filter(actif=True).count()
    factures_jour = Facture.objects.filter(date_creation__date=aujourd_hui).count()
    factures_impayees = Facture.objects.filter(statut='en_attente').count()

    paiements_jour = Paiement.objects.filter(date__date=aujourd_hui)
    encaisse_jour = sum(p.montant for p in paiements_jour)

    alertes_stock = StockAnnexe.objects.filter(
        quantite__lte=django_models.F('seuil_alerte')
    )

    mouvements_recents = MouvementStock.objects.select_related(
        'produit', 'annexe'
    ).order_by('-date')[:10]

    factures_en_attente = Facture.objects.filter(
        statut='en_attente'
    ).select_related('client')[:5]

    context = {
        'total_produits': total_produits,
        'factures_jour': factures_jour,
        'factures_impayees': factures_impayees,
        'encaisse_jour': encaisse_jour,
        'alertes_stock': alertes_stock,
        'mouvements_recents': mouvements_recents,
        'factures_en_attente': factures_en_attente,
    }
    return render(request, 'dashboard/index.html', context)