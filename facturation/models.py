from django.db import models
from produits.models import Produit
from accounts.models import Utilisateur, Annexe
from livraisons.models import Client


class Facture(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente de paiement'),
        ('payee', 'Payée'),
        ('partiellement_payee', 'Partiellement payée'),
        ('annulee', 'Annulée'),
    ]

    numero = models.CharField(max_length=50, unique=True)
    client = models.ForeignKey(
        Client, on_delete=models.PROTECT, related_name='factures'
    )
    annexe = models.ForeignKey(Annexe, on_delete=models.PROTECT)
    creee_par = models.ForeignKey(
        Utilisateur, on_delete=models.SET_NULL, null=True
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(
        max_length=25, choices=STATUT_CHOICES, default='en_attente'
    )
    note = models.TextField(blank=True)

    @property
    def montant_total(self):
        return sum(l.sous_total for l in self.lignes.all())

    @property
    def montant_paye(self):
        return sum(p.montant for p in self.paiements.all())

    @property
    def montant_restant(self):
        return self.montant_total - self.montant_paye

    def mettre_a_jour_statut(self):
        if self.montant_paye == 0:
            self.statut = 'en_attente'
        elif self.montant_paye >= self.montant_total:
            self.statut = 'payee'
        else:
            self.statut = 'partiellement_payee'
        self.save()

    def __str__(self):
        return f"Facture {self.numero} — {self.client} ({self.get_statut_display()})"


class LigneFacture(models.Model):
    facture = models.ForeignKey(
        Facture, on_delete=models.CASCADE, related_name='lignes'
    )
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    quantite = models.IntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def sous_total(self):
        return self.quantite * self.prix_unitaire

    def __str__(self):
        return f"{self.produit} x{self.quantite} = {self.sous_total} FCFA"