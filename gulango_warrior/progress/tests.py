from django.test import TestCase

from accounts.models import CustomUser
from avatars.models import Avatar
from .models import Conquista, AvatarConquista


class GanharXPConquistaTests(TestCase):
    def test_ganhar_xp_verifica_conquistas(self):
        user = CustomUser.objects.create_user(username="hero", password="123")
        avatar = Avatar.objects.create(user=user)

        conquista = Conquista.objects.create(
            nome="Iniciante",
            descricao="Ganhe 100 de XP",
            icone="conquistas/iniciante.png",
            condicao="xp_total >= 100",
        )

        avatar.ganhar_xp(100)

        self.assertTrue(
            AvatarConquista.objects.filter(avatar=avatar, conquista=conquista).exists()
        )
        self.assertEqual(avatar.xp_total, 100)
        self.assertEqual(avatar.nivel, 2)
