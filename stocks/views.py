from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import MouvementStock
from produits.models import Produit
from accounts.models import Annexe


@login_required
def entrees_stock(request):
    entrees = MouvementStock.objects.filter(
        type_mouvement='entree'
    ).select_related('produit', 'annexe', 'effectue_par').order_by('-date')[:50]

    return render(request, 'stocks/entrees.html', {'entrees': entrees})


@login_required
def ajouter_entree(request):
    produits = Produit.objects.filter(actif=True)
    annexes = Annexe.objects.all()

    if request.method == 'POST':
        produit_id = request.POST.get('produit')
        annexe_id = request.POST.get('annexe')
        quantite = request.POST.get('quantite')
        reference = request.POST.get('reference', '')
        note = request.POST.get('note', '')

        if not all([produit_id, annexe_id, quantite]):
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")
        else:
            MouvementStock.objects.create(
                produit_id=produit_id,
                annexe_id=annexe_id,
                type_mouvement='entree',
                quantite=int(quantite),
                effectue_par=request.user,
                reference=reference,
                note=note,
            )
            messages.success(request, "Entrée de stock enregistrée avec succès !")
            return redirect('entrees_stock')

    return render(request, 'stocks/form_entree.html', {
        'produits': produits,
        'annexes': annexes,
    })

@login_required
def sorties_stock(request):
    sorties = MouvementStock.objects.filter(
        type_mouvement__in=['sortie', 'vente_directe']
    ).select_related('produit', 'annexe', 'effectue_par').order_by('-date')[:50]

    return render(request, 'stocks/sorties.html', {'sorties': sorties})


@login_required
def ajouter_sortie(request):
    produits = Produit.objects.filter(actif=True)
    annexes = Annexe.objects.all()

    if request.method == 'POST':
        produit_id = request.POST.get('produit')
        annexe_id = request.POST.get('annexe')
        quantite = request.POST.get('quantite')
        type_mouvement = request.POST.get('type_mouvement', 'sortie')
        reference = request.POST.get('reference', '')
        note = request.POST.get('note', '')

        if not all([produit_id, annexe_id, quantite]):
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")
        else:
            from produits.models import StockAnnexe
            try:
                stock = StockAnnexe.objects.get(
                    produit_id=produit_id,
                    annexe_id=annexe_id
                )
                if stock.quantite < int(quantite):
                    messages.error(
                        request,
                        f"Stock insuffisant ! Stock disponible : {stock.quantite} unités."
                    )
                    return render(request, 'stocks/form_sortie.html', {
                        'produits': produits,
                        'annexes': annexes,
                    })
            except StockAnnexe.DoesNotExist:
                messages.error(request, "Aucun stock trouvé pour ce produit dans cette annexe.")
                return render(request, 'stocks/form_sortie.html', {
                    'produits': produits,
                    'annexes': annexes,
                })

            MouvementStock.objects.create(
                produit_id=produit_id,
                annexe_id=annexe_id,
                type_mouvement=type_mouvement,
                quantite=int(quantite),
                effectue_par=request.user,
                reference=reference,
                note=note,
            )
            messages.success(request, "Sortie de stock enregistrée avec succès !")
            return redirect('sorties_stock')

    return render(request, 'stocks/form_sortie.html', {
        'produits': produits,
        'annexes': annexes,
    })

@login_required
def transferts(request):
    from .models import Transfert
    liste = Transfert.objects.select_related(
        'produit', 'annexe_source', 'annexe_destination', 'effectue_par'
    ).order_by('-date')[:50]
    return render(request, 'stocks/transferts.html', {'transferts': liste})


@login_required
def ajouter_transfert(request):
    from .models import Transfert
    produits = Produit.objects.filter(actif=True)
    annexes = Annexe.objects.all()

    if request.method == 'POST':
        produit_id = request.POST.get('produit')
        source_id = request.POST.get('annexe_source')
        destination_id = request.POST.get('annexe_destination')
        quantite = request.POST.get('quantite')
        note = request.POST.get('note', '')

        if not all([produit_id, source_id, destination_id, quantite]):
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")
        elif source_id == destination_id:
            messages.error(request, "L'annexe source et destination doivent être différentes.")
        else:
            from produits.models import StockAnnexe
            try:
                stock = StockAnnexe.objects.get(
                    produit_id=produit_id,
                    annexe_id=source_id
                )
                if stock.quantite < int(quantite):
                    messages.error(
                        request,
                        f"Stock insuffisant dans l'annexe source ! Disponible : {stock.quantite} unités."
                    )
                    return render(request, 'stocks/form_transfert.html', {
                        'produits': produits, 'annexes': annexes
                    })
            except StockAnnexe.DoesNotExist:
                messages.error(request, "Aucun stock trouvé pour ce produit dans l'annexe source.")
                return render(request, 'stocks/form_transfert.html', {
                    'produits': produits, 'annexes': annexes
                })

            # Créer le transfert
            transfert = Transfert.objects.create(
                produit_id=produit_id,
                annexe_source_id=source_id,
                annexe_destination_id=destination_id,
                quantite=int(quantite),
                effectue_par=request.user,
                note=note,
            )

            # Mouvements de stock des deux côtés
            MouvementStock.objects.create(
                produit_id=produit_id,
                annexe_id=source_id,
                type_mouvement='transfert_sortie',
                quantite=int(quantite),
                effectue_par=request.user,
                reference=f"Transfert #{transfert.id}",
            )
            MouvementStock.objects.create(
                produit_id=produit_id,
                annexe_id=destination_id,
                type_mouvement='transfert_entree',
                quantite=int(quantite),
                effectue_par=request.user,
                reference=f"Transfert #{transfert.id}",
            )

            messages.success(request, "Transfert effectué avec succès !")
            return redirect('transferts')

    return render(request, 'stocks/form_transfert.html', {
        'produits': produits,
        'annexes': annexes,
    })