from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.ConnexionView.as_view(), name='login'),
    path('logout/', views.deconnexion, name='logout'),
]