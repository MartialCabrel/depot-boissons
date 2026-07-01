from django.db import models

class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Produit(models.Model):
    nom = models.CharField(max_length=100)
    categorie = models.ForeignKey(
        Categorie, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2)
    unite = models.CharField(max_length=50, help_text="Ex: palette, casier, bouteille")
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nom} ({self.unite})"


class StockAnnexe(models.Model):
    from accounts.models import Annexe
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    annexe = models.ForeignKey(Annexe, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=0)
    seuil_alerte = models.IntegerField(default=10)

    class Meta:
        unique_together = ('produit', 'annexe')

    def __str__(self):
        return f"{self.produit} — {self.annexe} : {self.quantite}"