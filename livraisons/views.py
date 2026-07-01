from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Client


@login_required
def liste_clients(request):
    clients = Client.objects.all().order_by('nom')
    return render(request, 'livraisons/clients.html', {'clients': clients})


@login_required
def ajouter_client(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        telephone = request.POST.get('telephone', '')
        adresse = request.POST.get('adresse', '')
        type_client = request.POST.get('type_client', 'habituel')

        if not nom:
            messages.error(request, "Le nom est obligatoire.")
        else:
            Client.objects.create(
                nom=nom,
                telephone=telephone,
                adresse=adresse,
                type_client=type_client,
            )
            messages.success(request, f"Client '{nom}' ajouté avec succès !")
            return redirect('liste_clients')

    return render(request, 'livraisons/form_client.html')


@login_required
def modifier_client(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        client.nom = request.POST.get('nom')
        client.telephone = request.POST.get('telephone', '')
        client.adresse = request.POST.get('adresse', '')
        client.type_client = request.POST.get('type_client', 'habituel')
        client.save()
        messages.success(request, f"Client '{client.nom}' modifié avec succès !")
        return redirect('liste_clients')

    return render(request, 'livraisons/form_client.html', {'client': client})


@login_required
def supprimer_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    nom = client.nom
    client.delete()
    messages.success(request, f"Client '{nom}' supprimé.")
    return redirect('liste_clients')

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Client, Tournee, LigneTournee
from produits.models import Produit
from accounts.models import Utilisateur, Annexe
from stocks.models import MouvementStock


@login_required
def liste_tournees(request):
    tournees = Tournee.objects.select_related(
        'livreur', 'annexe'
    ).order_by('-date')[:50]
    return render(request, 'livraisons/tournees.html', {'tournees': tournees})


@login_required
def creer_tournee(request):
    livreurs = Utilisateur.objects.filter(role='livreur')
    annexes = Annexe.objects.all()
    produits = Produit.objects.filter(actif=True)

    if request.method == 'POST':
        livreur_id = request.POST.get('livreur')
        annexe_id = request.POST.get('annexe')
        produit_ids = request.POST.getlist('produit_id')
        quantites = request.POST.getlist('quantite_chargee')

        if not all([livreur_id, annexe_id]):
            messages.error(request, "Livreur et annexe sont obligatoires.")
            return render(request, 'livraisons/form_tournee.html', {
                'livreurs': livreurs, 'annexes': annexes, 'produits': produits
            })

        if not produit_ids:
            messages.error(request, "Ajoutez au moins un produit.")
            return render(request, 'livraisons/form_tournee.html', {
                'livreurs': livreurs, 'annexes': annexes, 'produits': produits
            })

        tournee = Tournee.objects.create(
            livreur_id=livreur_id,
            annexe_id=annexe_id,
            statut='en_cours',
        )

        for pid, qte in zip(produit_ids, quantites):
            if pid and qte and int(qte) > 0:
                LigneTournee.objects.create(
                    tournee=tournee,
                    produit_id=pid,
                    quantite_chargee=int(qte),
                )
                # Sortie de stock immédiate au chargement
                MouvementStock.objects.create(
                    produit_id=pid,
                    annexe_id=annexe_id,
                    type_mouvement='sortie',
                    quantite=int(qte),
                    effectue_par=request.user,
                    reference=f"Tournée #{tournee.id}",
                )

        messages.success(request, f"Tournée #{tournee.id} créée avec succès !")
        return redirect('detail_tournee', pk=tournee.pk)

    return render(request, 'livraisons/form_tournee.html', {
        'livreurs': livreurs,
        'annexes': annexes,
        'produits': produits,
    })


@login_required
def detail_tournee(request, pk):
    tournee = get_object_or_404(
        Tournee.objects.select_related('livreur', 'annexe'), pk=pk
    )
    lignes = tournee.lignes.select_related('produit').all()
    return render(request, 'livraisons/detail_tournee.html', {
        'tournee': tournee,
        'lignes': lignes,
    })


@login_required
def cloturer_tournee(request, pk):
    tournee = get_object_or_404(Tournee, pk=pk)

    if tournee.statut == 'terminee':
        messages.warning(request, "Cette tournée est déjà clôturée.")
        return redirect('detail_tournee', pk=pk)

    if request.method == 'POST':
        lignes = tournee.lignes.all()

        for ligne in lignes:
            qte_vendue = int(request.POST.get(f'vendue_{ligne.id}', 0))
            qte_retournee = int(request.POST.get(f'retournee_{ligne.id}', 0))

            # Validation
            if qte_vendue + qte_retournee > ligne.quantite_chargee:
                messages.error(
                    request,
                    f"Erreur sur {ligne.produit} : vendu + retourné > chargé !"
                )
                return redirect('detail_tournee', pk=pk)

            ligne.quantite_vendue = qte_vendue
            ligne.quantite_retournee = qte_retournee
            ligne.save()

            # Retour en stock des invendus
            if qte_retournee > 0:
                MouvementStock.objects.create(
                    produit=ligne.produit,
                    annexe=tournee.annexe,
                    type_mouvement='retour',
                    quantite=qte_retournee,
                    effectue_par=request.user,
                    reference=f"Retour Tournée #{tournee.id}",
                )

        tournee.statut = 'terminee'
        tournee.save()
        messages.success(request, f"Tournée #{tournee.id} clôturée avec succès !")
        return redirect('detail_tournee', pk=pk)

    return redirect('detail_tournee', pk=pk)