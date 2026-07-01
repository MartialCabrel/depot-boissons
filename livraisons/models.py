from django.db import models
from produits.models import Produit
from accounts.models import Utilisateur, Annexe


class Tournee(models.Model):
    """Représente une sortie journalière d'un livreur avec son tricycle"""
    STATUT_CHOICES = [
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]

    livreur = models.ForeignKey(
        Utilisateur, on_delete=models.PROTECT, related_name='tournees'
    )
    annexe = models.ForeignKey(Annexe, on_delete=models.PROTECT)
    date = models.DateField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_cours')
    note = models.TextField(blank=True)

    def __str__(self):
        return f"Tournée {self.livreur} — {self.date:%d/%m/%Y} ({self.get_statut_display()})"


class LigneTournee(models.Model):
    """Chaque produit chargé dans la tournée"""
    tournee = models.ForeignKey(
        Tournee, on_delete=models.CASCADE, related_name='lignes'
    )
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    quantite_chargee = models.IntegerField()
    quantite_vendue = models.IntegerField(default=0)
    quantite_retournee = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.produit} — chargé: {self.quantite_chargee} | vendu: {self.quantite_vendue} | retour: {self.quantite_retournee}"

    @property
    def quantite_non_comptabilisee(self):
        """Détecte les écarts : chargé ≠ vendu + retourné"""
        return self.quantite_chargee - self.quantite_vendue - self.quantite_retournee


class Client(models.Model):
    TYPE_CHOICES = [
        ('habituel', 'Client habituel'),
        ('occasionnel', 'Client occasionnel'),
    ]

    nom = models.CharField(max_length=150)
    telephone = models.CharField(max_length=15, blank=True)
    adresse = models.TextField(blank=True)
    type_client = models.CharField(max_length=20, choices=TYPE_CHOICES, default='habituel')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} ({self.get_type_client_display()})"