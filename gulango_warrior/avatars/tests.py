from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from .models import Avatar, SkinVisual, SkinUsuario


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


class SkinUsuarioModelTests(TestCase):
    def test_create_skin_usuario(self):
        user = CustomUser.objects.create_user(username="u", password="p")
        skin = SkinVisual.objects.create(
            nome="Robe Vermelho",
            tipo="avatar",
            imagem="skins/robe.png",
            preco_moedas=10,
            classe_restrita="todas",
        )
        skin_usuario = SkinUsuario.objects.create(usuario=user, skin=skin)

        self.assertTrue(SkinUsuario.objects.filter(id=skin_usuario.id).exists())
        self.assertEqual(str(skin_usuario), "u - Robe Vermelho")


class ComprarSkinTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="buyer", password="123")
        self.avatar = Avatar.objects.create(user=self.user, moedas=20)
        self.skin1 = SkinVisual.objects.create(
            nome="Armadura A",
            tipo=SkinVisual.TIPO_AVATAR,
            imagem="skins/a.png",
            preco_moedas=10,
            classe_restrita="todas",
        )
        self.skin2 = SkinVisual.objects.create(
            nome="Armadura B",
            tipo=SkinVisual.TIPO_AVATAR,
            imagem="skins/b.png",
            preco_moedas=5,
            classe_restrita="todas",
        )

    def test_compra_primeira_skin_em_uso(self):
        from .utils import comprar_skin

        resultado = comprar_skin(self.user, self.skin1)
        self.assertTrue(resultado)
        self.avatar.refresh_from_db()
        self.assertEqual(self.avatar.moedas, 10)
        skin_usuario = SkinUsuario.objects.get(usuario=self.user, skin=self.skin1)
        self.assertTrue(skin_usuario.em_uso)

    def test_compra_segunda_skin_nao_em_uso(self):
        from .utils import comprar_skin

        comprar_skin(self.user, self.skin1)
        self.avatar.refresh_from_db()
        resultado = comprar_skin(self.user, self.skin2)
        self.assertTrue(resultado)
        skin_usuario = SkinUsuario.objects.get(usuario=self.user, skin=self.skin2)
        self.assertFalse(skin_usuario.em_uso)

    def test_compra_sem_moedas(self):
        from .utils import comprar_skin

        self.avatar.moedas = 5
        self.avatar.save()
        resultado = comprar_skin(self.user, self.skin1)
        self.assertFalse(resultado)
        self.assertFalse(
            SkinUsuario.objects.filter(usuario=self.user, skin=self.skin1).exists()
        )
