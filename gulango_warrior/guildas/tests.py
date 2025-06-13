from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from .models import Guilda, MembroGuilda


class CriarGuildaViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="guerreiro", password="123")

    def test_login_required(self):
        response = self.client.get(reverse("criar_guilda"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_criar_guilda(self):
        self.client.login(username="guerreiro", password="123")
        with open(__file__, 'rb') as f:
            response = self.client.post(
                reverse("criar_guilda"),
                {
                    "nome": "Legiao",
                    "descricao": "Bravos",
                    "brasao": f,
                },
            )
        self.assertRedirects(response, reverse("criar_guilda"))
        guilda = Guilda.objects.get(nome="Legiao")
        self.assertEqual(guilda.lider, self.user)
        self.assertTrue(MembroGuilda.objects.filter(usuario=self.user, guilda=guilda, cargo=MembroGuilda.CARGO_LIDER).exists())

    def test_ja_e_membro(self):
        guilda = Guilda.objects.create(nome="G1", descricao="D", brasao="b.png", lider=self.user)
        MembroGuilda.objects.create(usuario=self.user, guilda=guilda, cargo=MembroGuilda.CARGO_LIDER)
        self.client.login(username="guerreiro", password="123")
        response = self.client.post(reverse("criar_guilda"), {"nome": "X", "descricao": "Y"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "já pertence")
