from django.urls import path
from . import views

urlpatterns = [
    path('clients/', views.liste_clients, name='liste_clients'),
    path('clients/ajouter/', views.ajouter_client, name='ajouter_client'),
    path('clients/modifier/<int:pk>/', views.modifier_client, name='modifier_client'),
    path('clients/supprimer/<int:pk>/', views.supprimer_client, name='supprimer_client'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('clients/', views.liste_clients, name='liste_clients'),
    path('clients/ajouter/', views.ajouter_client, name='ajouter_client'),
    path('clients/modifier/<int:pk>/', views.modifier_client, name='modifier_client'),
    path('clients/supprimer/<int:pk>/', views.supprimer_client, name='supprimer_client'),
    path('tournees/', views.liste_tournees, name='liste_tournees'),
    path('tournees/creer/', views.creer_tournee, name='creer_tournee'),
    path('tournees/<int:pk>/', views.detail_tournee, name='detail_tournee'),
    path('tournees/<int:pk>/cloturer/', views.cloturer_tournee, name='cloturer_tournee'),
]