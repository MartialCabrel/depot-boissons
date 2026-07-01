from django.db import models
from accounts.models import Utilisateur, Annexe
from facturation.models import Facture


class Paiement(models.Model):
    MODE_CHOICES = [
        ('cash', 'Espèces'),
        ('mtn_momo', 'MTN Mobile Money'),
        ('orange_money', 'Orange Money'),
    ]

    facture = models.ForeignKey(
        Facture, on_delete=models.PROTECT, related_name='paiements'
    )
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    mode_paiement = models.CharField(max_length=20, choices=MODE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    encaisse_par = models.ForeignKey(
        Utilisateur, on_delete=models.SET_NULL, null=True
    )
    reference_transaction = models.CharField(
        max_length=100, blank=True,
        help_text="Référence MoMo si paiement mobile"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Mettre à jour le statut de la facture automatiquement
        self.facture.mettre_a_jour_statut()

    def __str__(self):
        return f"Paiement {self.montant} FCFA — {self.get_mode_paiement_display()} ({self.date:%d/%m/%Y})"


class SessionCaisse(models.Model):
    """Représente une journée de caisse"""
    STATUT_CHOICES = [
        ('ouverte', 'Ouverte'),
        ('fermee', 'Fermée'),
    ]

    caissiere = models.ForeignKey(
        Utilisateur, on_delete=models.PROTECT, related_name='sessions_caisse'
    )
    annexe = models.ForeignKey(Annexe, on_delete=models.PROTECT)
    date_ouverture = models.DateTimeField(auto_now_add=True)
    date_fermeture = models.DateTimeField(null=True, blank=True)
    montant_ouverture = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        help_text="Fond de caisse au départ"
    )
    statut = models.CharField(
        max_length=10, choices=STATUT_CHOICES, default='ouverte'
    )

    @property
    def total_encaisse(self):
        paiements = Paiement.objects.filter(
            encaisse_par=self.caissiere,
            date__date=self.date_ouverture.date()
        )
        return sum(p.montant for p in paiements)

    def __str__(self):
        return f"Caisse {self.caissiere} — {self.date_ouverture:%d/%m/%Y} ({self.get_statut_display()})"