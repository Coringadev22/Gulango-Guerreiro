from .models import Notificacao


def notificacoes(request):
    if request.user.is_authenticated:
        qs = Notificacao.objects.filter(usuario=request.user).order_by('-data')
        recentes = list(qs[:5])
        nao_lidas = qs.filter(lida=False).count()
    else:
        recentes = []
        nao_lidas = 0
    return {
        'notificacoes_recentes': recentes,
        'notificacoes_nao_lidas': nao_lidas,
    }
