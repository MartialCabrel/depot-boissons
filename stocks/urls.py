from django.urls import path
from . import views

urlpatterns = [
    path('entrees/', views.entrees_stock, name='entrees_stock'),
    path('entrees/ajouter/', views.ajouter_entree, name='ajouter_entree'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('entrees/', views.entrees_stock, name='entrees_stock'),
    path('entrees/ajouter/', views.ajouter_entree, name='ajouter_entree'),
    path('sorties/', views.sorties_stock, name='sorties_stock'),
    path('sorties/ajouter/', views.ajouter_sortie, name='ajouter_sortie'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('entrees/', views.entrees_stock, name='entrees_stock'),
    path('entrees/ajouter/', views.ajouter_entree, name='ajouter_entree'),
    path('sorties/', views.sorties_stock, name='sorties_stock'),
    path('sorties/ajouter/', views.ajouter_sortie, name='ajouter_sortie'),
    path('transferts/', views.transferts, name='transferts'),
    path('transferts/ajouter/', views.ajouter_transfert, name='ajouter_transfert'),
]