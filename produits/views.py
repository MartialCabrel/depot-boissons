from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Produit, Categorie

UNITES = [
    ('palette', 'Palette'),
    ('casier', 'Casier'),
    ('bouteille', 'Bouteille'),
    ('carton', 'Carton'),
    ('pack', 'Pack'),
]


@login_required
def liste_produits(request):
    produits = Produit.objects.select_related('categorie').filter(actif=True)
    categories = Categorie.objects.all()
    return render(request, 'produits/liste.html', {
        'produits': produits,
        'categories': categories
    })


@login_required
def ajouter_produit(request):
    categories = Categorie.objects.all()
    if request.method == 'POST':
        nom = request.POST.get('nom')
        categorie_id = request.POST.get('categorie')
        prix_vente = request.POST.get('prix_vente')
        unite = request.POST.get('unite')

        if not all([nom, prix_vente, unite]):
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")
            return render(request, 'produits/form.html', {
                'categories': categories,
                'unites': UNITES
            })

        Produit.objects.create(
            nom=nom,
            categorie_id=categorie_id if categorie_id else None,
            prix_vente=prix_vente,
            unite=unite,
        )
        messages.success(request, f"Produit '{nom}' ajouté avec succès !")
        return redirect('liste_produits')

    return render(request, 'produits/form.html', {
        'categories': categories,
        'unites': UNITES
    })


@login_required
def modifier_produit(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    categories = Categorie.objects.all()

    if request.method == 'POST':
        produit.nom = request.POST.get('nom')
        produit.categorie_id = request.POST.get('categorie') or None
        produit.prix_vente = request.POST.get('prix_vente')
        produit.unite = request.POST.get('unite')
        produit.save()
        messages.success(request, f"Produit '{produit.nom}' modifié avec succès !")
        return redirect('liste_produits')

    return render(request, 'produits/form.html', {
        'produit': produit,
        'categories': categories,
        'unites': UNITES
    })


@login_required
def supprimer_produit(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    produit.actif = False
    produit.save()
    messages.success(request, f"Produit '{produit.nom}' supprimé.")
    return redirect('liste_produits')