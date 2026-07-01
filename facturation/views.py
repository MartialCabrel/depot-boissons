from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Facture, LigneFacture
from livraisons.models import Client
from produits.models import Produit
from accounts.models import Annexe
import uuid


def generer_numero_facture():
    return f"FAC-{uuid.uuid4().hex[:8].upper()}"


@login_required
def liste_factures(request):
    statut = request.GET.get('statut', '')
    factures = Facture.objects.select_related(
        'client', 'annexe', 'creee_par'
    ).order_by('-date_creation')

    if statut:
        factures = factures.filter(statut=statut)

    return render(request, 'facturation/liste.html', {
        'factures': factures,
        'statut_filtre': statut,
    })


@login_required
def creer_facture(request):
    clients = Client.objects.all().order_by('nom')
    produits = Produit.objects.filter(actif=True)
    annexes = Annexe.objects.all()

    if request.method == 'POST':
        client_id = request.POST.get('client')
        annexe_id = request.POST.get('annexe')
        note = request.POST.get('note', '')
        produit_ids = request.POST.getlist('produit_id')
        quantites = request.POST.getlist('quantite')
        prix = request.POST.getlist('prix_unitaire')

        if not all([client_id, annexe_id]):
            messages.error(request, "Client et annexe sont obligatoires.")
            return render(request, 'facturation/form_facture.html', {
                'clients': clients, 'produits': produits, 'annexes': annexes
            })

        if not produit_ids:
            messages.error(request, "Ajoutez au moins un produit à la facture.")
            return render(request, 'facturation/form_facture.html', {
                'clients': clients, 'produits': produits, 'annexes': annexes
            })

        facture = Facture.objects.create(
            numero=generer_numero_facture(),
            client_id=client_id,
            annexe_id=annexe_id,
            creee_par=request.user,
            note=note,
        )

        for pid, qte, pu in zip(produit_ids, quantites, prix):
            if pid and qte and pu:
                LigneFacture.objects.create(
                    facture=facture,
                    produit_id=pid,
                    quantite=int(qte),
                    prix_unitaire=pu,
                )

        messages.success(request, f"Facture {facture.numero} créée avec succès !")
        return redirect('detail_facture', pk=facture.pk)

    return render(request, 'facturation/form_facture.html', {
        'clients': clients,
        'produits': produits,
        'annexes': annexes,
    })


@login_required
def detail_facture(request, pk):
    facture = get_object_or_404(
        Facture.objects.select_related('client', 'annexe', 'creee_par'),
        pk=pk
    )
    lignes = facture.lignes.select_related('produit').all()
    paiements = facture.paiements.all()

    return render(request, 'facturation/detail.html', {
        'facture': facture,
        'lignes': lignes,
        'paiements': paiements,
    })


@login_required
def ajouter_paiement(request, pk):
    from caisse.models import Paiement
    facture = get_object_or_404(Facture, pk=pk)

    if request.method == 'POST':
        montant = request.POST.get('montant')
        mode_paiement = request.POST.get('mode_paiement')
        reference = request.POST.get('reference_transaction', '')

        if not all([montant, mode_paiement]):
            messages.error(request, "Montant et mode de paiement sont obligatoires.")
            return redirect('detail_facture', pk=pk)
        elif float(montant) > float(facture.montant_restant):
            messages.error(
                request,
                f"Montant trop élevé ! Le reste à payer est de {facture.montant_restant} F."
            )
            return redirect('detail_facture', pk=pk)
        else:
            Paiement.objects.create(
                facture=facture,
                montant=montant,
                mode_paiement=mode_paiement,
                reference_transaction=reference,
                encaisse_par=request.user,
            )
            messages.success(request, "Paiement enregistré avec succès !")

    return redirect('detail_facture', pk=pk)