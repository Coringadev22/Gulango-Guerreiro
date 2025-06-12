from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from avatars.models import Avatar
from .models import Item, CompraItem


class LojaViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="player", password="123")
        self.avatar = Avatar.objects.create(user=self.user, classe="guerreiro", moedas=50)
        self.item = Item.objects.create(
            nome="Espada",
            descricao="Uma espada afiada",
            preco=30,
            imagem="itens/espada.png",
            classe_restrita="guerreiro",
        )

    def test_loja_get(self):
        self.client.login(username="player", password="123")
        response = self.client.get(reverse("loja_view"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.nome)

    def test_comprar_item_sucesso(self):
        self.client.login(username="player", password="123")
        response = self.client.post(reverse("loja_view"), {"item_id": self.item.id})
        self.assertRedirects(response, reverse("loja_view"))
        self.avatar.refresh_from_db()
        self.assertEqual(self.avatar.moedas, 20)
        self.assertEqual(CompraItem.objects.count(), 1)

