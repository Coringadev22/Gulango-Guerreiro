from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

from accounts.models import CustomUser
from .models import Course, Lesson, NPC, HistoricoDialogo


class CourseViewsTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="p", password="1")
        self.course = Course.objects.create(
            title="Magia",
            description="A",
            instructor=self.user,
            linguagem=Course.LING_GOLANG,
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title="Intro",
            video_url="http://example.com",
            order=1,
        )

    def test_mapa_mundi_login_required(self):
        response = self.client.get(reverse("mapa_mundi"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_conversar_npc_login_required(self):
        npc = NPC.objects.create(
            nome="Guardião",
            avatar="npcs/g.png",
            curso=self.course,
            frase_inicial="Olá",
            tipo=NPC.FIXO,
        )
        response = self.client.get(reverse("conversar_npc", args=[npc.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_conversar_npc_fixo(self):
        npc = NPC.objects.create(
            nome="Guardião",
            avatar="npcs/g.png",
            curso=self.course,
            frase_inicial="Olá",
            tipo=NPC.FIXO,
        )

        self.client.login(username="p", password="1")
        response = self.client.post(
            reverse("conversar_npc", args=[npc.id]), {"pergunta": "Oi"}
        )
        self.assertContains(response, "Olá")
        self.assertTrue(
            HistoricoDialogo.objects.filter(usuario=self.user, npc=npc).exists()
        )

    def test_conversar_npc_ia(self):
        npc = NPC.objects.create(
            nome="Mago",
            avatar="npcs/m.png",
            curso=self.course,
            frase_inicial="Oi",
            tipo=NPC.IA,
        )

        with patch("courses.views.gerar_resposta_ia", return_value="resposta"):
            self.client.login(username="p", password="1")
            response = self.client.post(
                reverse("conversar_npc", args=[npc.id]), {"pergunta": "?"}
            )
            self.assertContains(response, "resposta")

