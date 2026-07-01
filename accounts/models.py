from django.contrib.auth.models import AbstractUser
from django.db import models

class Utilisateur(AbstractUser):
    ROLES = [
        ('responsable', 'Responsable'),
        ('superviseur', 'Superviseur'),
        ('facturiere', 'Facturière'),
        ('caissiere', 'Caissière'),
        ('magasinier', 'Magasinier'),
        ('livreur', 'Livreur'),
    ]
    role = models.CharField(max_length=20, choices=ROLES)
    telephone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"


class Annexe(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.TextField(blank=True)
    responsable = models.ForeignKey(
        Utilisateur, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='annexes_gerees'
    )

    def __str__(self):
        return self.nom