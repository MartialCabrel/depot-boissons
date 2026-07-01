from django.urls import path
from . import views

urlpatterns = [
    path('journalier/', views.rapport_journalier, name='rapport_journalier'),
    path('hebdomadaire/', views.rapport_hebdomadaire, name='rapport_hebdomadaire'),
    path('mensuel/', views.rapport_mensuel, name='rapport_mensuel'),
    path('export/<str:type_rapport>/pdf/', views.export_pdf, name='export_pdf'),
    path('export/<str:type_rapport>/excel/', views.export_excel, name='export_excel'),
]