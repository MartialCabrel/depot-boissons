from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Paiement, SessionCaisse
from accounts.models import Annexe


@login_required
def tableau_caisse(request):
    aujourd_hui = timezone.now().date()

    # Paiements du jour
    paiements = Paiement.objects.filter(
        date__date=aujourd_hui
    ).select_related('facture', 'facture__client', 'encaisse_par').order_by('-date')

    # Totaux par mode
    total_cash = sum(p.montant for p in paiements if p.mode_paiement == 'cash')
    total_mtn = sum(p.montant for p in paiements if p.mode_paiement == 'mtn_momo')
    total_orange = sum(p.montant for p in paiements if p.mode_paiement == 'orange_money')
    total_jour = total_cash + total_mtn + total_orange

    # Session ouverte
    session = SessionCaisse.objects.filter(
        date_ouverture__date=aujourd_hui,
        statut='ouverte'
    ).first()

    return render(request, 'caisse/tableau.html', {
        'paiements': paiements,
        'total_cash': total_cash,
        'total_mtn': total_mtn,
        'total_orange': total_orange,
        'total_jour': total_jour,
        'session': session,
        'aujourd_hui': aujourd_hui,
    })


@login_required
def ouvrir_session(request):
    annexes = Annexe.objects.all()
    aujourd_hui = timezone.now().date()

    # Vérifier si session déjà ouverte
    session_existante = SessionCaisse.objects.filter(
        date_ouverture__date=aujourd_hui,
        statut='ouverte'
    ).first()

    if session_existante:
        messages.warning(request, "Une session de caisse est déjà ouverte aujourd'hui.")
        return redirect('tableau_caisse')

    if request.method == 'POST':
        annexe_id = request.POST.get('annexe')
        montant_ouverture = request.POST.get('montant_ouverture', 0)

        SessionCaisse.objects.create(
            caissiere=request.user,
            annexe_id=annexe_id,
            montant_ouverture=montant_ouverture,
            statut='ouverte',
        )
        messages.success(request, "Session de caisse ouverte avec succès !")
        return redirect('tableau_caisse')

    return render(request, 'caisse/form_session.html', {'annexes': annexes})


@login_required
def fermer_session(request, pk):
    session = get_object_or_404(SessionCaisse, pk=pk)
    session.statut = 'fermee'
    session.date_fermeture = timezone.now()
    session.save()
    messages.success(request, "Session de caisse fermée.")
    return redirect('tableau_caisse')