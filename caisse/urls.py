from django.urls import path
from . import views

urlpatterns = [
    path('', views.tableau_caisse, name='tableau_caisse'),
    path('ouvrir/', views.ouvrir_session, name='ouvrir_session'),
    path('fermer/<int:pk>/', views.fermer_session, name='fermer_session'),
]