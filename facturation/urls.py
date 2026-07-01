from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_factures, name='liste_factures'),
    path('creer/', views.creer_facture, name='creer_facture'),
    path('<int:pk>/', views.detail_facture, name='detail_facture'),
    path('<int:pk>/paiement/', views.ajouter_paiement, name='ajouter_paiement'),
]