from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.shortcuts import render

from accounts.models import CustomUser
from avatars.models import Avatar
from progress.models import AvatarConquista


@staff_member_required
def admin_dashboard(request):
    """Display overall game statistics for administrators."""

    total_users = CustomUser.objects.count()
    total_xp = Avatar.objects.aggregate(total=Sum('xp_total')).get('total') or 0
    total_conquistas = AvatarConquista.objects.count()
    total_moedas = Avatar.objects.aggregate(total=Sum('moedas')).get('total') or 0
    top_players = Avatar.objects.select_related('user').order_by('-xp_total')[:3]

    context = {
        'total_users': total_users,
        'total_xp': total_xp,
        'total_conquistas': total_conquistas,
        'total_moedas': total_moedas,
        'top_players': top_players,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)
