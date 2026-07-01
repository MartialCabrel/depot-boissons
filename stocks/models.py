from django.db import models
from produits.models import Produit, StockAnnexe
from accounts.models import Utilisateur, Annexe


class MouvementStock(models.Model):
    TYPE_CHOICES = [
        ('entree', 'Entrée fournisseur'),
        ('sortie', 'Sortie livraison'),
        ('retour', 'Retour invendu'),
        ('transfert_sortie', 'Transfert sortant'),
        ('transfert_entree', 'Transfert entrant'),
        ('vente_directe', 'Vente directe'),
        ('ajustement', 'Ajustement inventaire'),
    ]

    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    annexe = models.ForeignKey(Annexe, on_delete=models.PROTECT)
    type_mouvement = models.CharField(max_length=20, choices=TYPE_CHOICES)
    quantite = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    effectue_par = models.ForeignKey(
        Utilisateur, on_delete=models.SET_NULL, null=True
    )
    reference = models.CharField(max_length=100, blank=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_type_mouvement_display()} — {self.produit} x{self.quantite} ({self.date:%d/%m/%Y})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Mettre à jour le stock automatiquement
        stock, _ = StockAnnexe.objects.get_or_create(
            produit=self.produit,
            annexe=self.annexe
        )
        if self.type_mouvement in ('entree', 'retour', 'transfert_entree'):
            stock.quantite += self.quantite
        elif self.type_mouvement in ('sortie', 'transfert_sortie', 'vente_directe', 'ajustement'):
            nouveau_stock = stock.quantite - self.quantite
            if nouveau_stock < 0:
                raise ValueError(
                    f"Stock insuffisant pour {self.produit} ! "
                    f"Disponible : {stock.quantite}, demandé : {self.quantite}"
                )
            stock.quantite = nouveau_stock
        stock.save()


class Transfert(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    annexe_source = models.ForeignKey(
        Annexe, on_delete=models.PROTECT, related_name='transferts_sortants'
    )
    annexe_destination = models.ForeignKey(
        Annexe, on_delete=models.PROTECT, related_name='transferts_entrants'
    )
    quantite = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    effectue_par = models.ForeignKey(
        Utilisateur, on_delete=models.SET_NULL, null=True
    )
    note = models.TextField(blank=True)

    def __str__(self):
        return f"Transfert {self.produit} x{self.quantite} : {self.annexe_source} → {self.annexe_destination}"