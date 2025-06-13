from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from .models import Avatar, SkinVisual


class AvatarModelTests(TestCase):
    def test_ganhar_xp_sobe_nivel(self):
        user = CustomUser.objects.create_user(username="player", password="123")
        avatar = Avatar.objects.create(user=user)

        avatar.ganhar_xp(50)
        self.assertEqual(avatar.xp_total, 50)
        self.assertEqual(avatar.nivel, 1)

        avatar.ganhar_xp(60)
        avatar.refresh_from_db()
        self.assertEqual(avatar.nivel, 2)

    def test_str(self):
        user = CustomUser.objects.create_user(username="knight", password="123")
        avatar = Avatar.objects.create(user=user, nivel=3)
        self.assertEqual(str(avatar), "knight - Nível 3")


class AvatarViewSecurityTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="a", password="b")
        Avatar.objects.create(user=self.user)

    def test_views_require_login(self):
        for name in ["perfil_avatar", "ranking_geral", "destaque_conquistas"]:
            url = reverse(name)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn("/accounts/login/", response["Location"])


class SkinVisualModelTests(TestCase):
    def test_str(self):
        skin = SkinVisual.objects.create(
            nome="Capa Azul",
            tipo="avatar",
            imagem="skins/capa.png",
            preco_moedas=5,
            classe_restrita="todas",
        )
        self.assertEqual(str(skin), "Capa Azul")
