from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur, Annexe

@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ('username', 'get_full_name', 'role', 'telephone', 'is_active')
    list_filter = ('role',)
    fieldsets = UserAdmin.fieldsets + (
        ('Informations dépôt', {'fields': ('role', 'telephone')}),
    )

@admin.register(Annexe)
class AnnexeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'adresse', 'responsable')