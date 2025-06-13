from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from avatars.models import Avatar
from django.core.files.uploadedfile import SimpleUploadedFile
from courses.models import Course, Lesson
from datetime import date
from django.utils import timezone

from .models import (
    Conquista,
    AvatarConquista,
    MissaoDiaria,
    UsuarioMissao,
    Notificacao,
    ProgressoPorLinguagem,
    Certificado,
    LessonProgress,
    Duelo,
    PerguntaDuelo,
)
from .utils import verificar_missoes_automaticas


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


class UsuarioMissaoModelTests(TestCase):
    def test_criacao_usuario_missao(self):
        user = CustomUser.objects.create_user(username="teste", password="123")
        missao = MissaoDiaria.objects.create(
            descricao="Testar",
            xp_recompensa=10,
            moedas_recompensa=5,
            condicao="",
        )
        usuario_missao = UsuarioMissao.objects.create(
            usuario=user,
            missao=missao,
            concluida=True,
            data=date.today(),
        )

        self.assertTrue(UsuarioMissao.objects.filter(id=usuario_missao.id).exists())


class MissoesDoDiaViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="player", password="123")
        self.avatar = Avatar.objects.create(user=self.user)
        self.missao = MissaoDiaria.objects.create(
            descricao="Ganhar XP",
            xp_recompensa=10,
            moedas_recompensa=5,
            condicao="",
        )

    def test_missoes_get(self):
        self.client.login(username="player", password="123")
        response = self.client.get(reverse("missoes_diarias"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.missao.descricao)

    def test_concluir_missao(self):
        self.client.login(username="player", password="123")
        response = self.client.post(
            reverse("missoes_diarias"),
            {
                "missao_id": self.missao.id,
                "linguagem": ProgressoPorLinguagem.LING_GOLANG,
            },
        )
        self.assertRedirects(response, reverse("missoes_diarias"))
        self.avatar.refresh_from_db()
        self.assertEqual(self.avatar.xp_total, 10)
        self.assertEqual(self.avatar.moedas, 5)
        self.assertTrue(
            UsuarioMissao.objects.filter(
                usuario=self.user,
                missao=self.missao,
                data=date.today(),
                concluida=True,
            ).exists()
        )
        progresso = ProgressoPorLinguagem.objects.get(
            usuario=self.user, linguagem=ProgressoPorLinguagem.LING_GOLANG
        )
        self.assertEqual(progresso.xp_total, 10)


class VerificarMissoesAutomaticasTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="auto", password="123")
        self.avatar = Avatar.objects.create(user=self.user)
        self.missao = MissaoDiaria.objects.create(
            descricao="Ganhar 10 XP",
            xp_recompensa=5,
            moedas_recompensa=2,
            condicao="xp_total >= 10",
        )

    def test_verificar_missoes(self):
        verificar_missoes_automaticas(
            self.user, {"linguagem": ProgressoPorLinguagem.LING_GOLANG}
        )
        usuario_missao = UsuarioMissao.objects.get(
            usuario=self.user, missao=self.missao, data=date.today()
        )
        self.assertFalse(usuario_missao.concluida)

        self.avatar.ganhar_xp(10, linguagem=ProgressoPorLinguagem.LING_GOLANG)
        verificar_missoes_automaticas(
            self.user, {"linguagem": ProgressoPorLinguagem.LING_GOLANG}
        )

        usuario_missao = UsuarioMissao.objects.get(
            usuario=self.user, missao=self.missao, data=date.today()
        )
        self.assertTrue(usuario_missao.concluida)
        self.avatar.refresh_from_db()
        self.assertEqual(self.avatar.xp_total, 15)
        self.assertEqual(self.avatar.moedas, 2)
        progresso = ProgressoPorLinguagem.objects.get(
            usuario=self.user, linguagem=ProgressoPorLinguagem.LING_GOLANG
        )
        self.assertEqual(progresso.xp_total, 15)


class FeedbackPersonalizadoViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="fb", password="123")
        Avatar.objects.create(user=self.user)

    def test_feedback_view(self):
        self.client.login(username="fb", password="123")
        response = self.client.get(reverse("feedback_personalizado"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("mensagem", response.context)


class NotificacaoModelTests(TestCase):
    def test_str(self):
        user = CustomUser.objects.create_user(username="n", password="p")
        notificacao = Notificacao.objects.create(
            usuario=user,
            titulo="Boas vindas",
            mensagem="Bem-vindo ao jogo",
            tipo="sistema",
        )
        self.assertEqual(str(notificacao), "Boas vindas")


class NotificacoesUsuarioViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="nu", password="123")
        self.notificacao = Notificacao.objects.create(
            usuario=self.user,
            titulo="Sauda\u00e7\u00e3o",
            mensagem="Oi",
            tipo="sistema",
        )

    def test_login_required(self):
        response = self.client.get(reverse("notificacoes_usuario"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_listar_e_marcar(self):
        self.client.login(username="nu", password="123")
        # GET list
        response = self.client.get(reverse("notificacoes_usuario"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sauda\u00e7\u00e3o")

        # Mark as read
        response = self.client.post(
            reverse("notificacoes_usuario"), {"notificacao_id": self.notificacao.id}
        )
        self.assertRedirects(response, reverse("notificacoes_usuario"))
        self.notificacao.refresh_from_db()
        self.assertTrue(self.notificacao.lida)


class PainelLinguagensViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="pl", password="123")
        Avatar.objects.create(user=self.user)
        ProgressoPorLinguagem.objects.create(
            usuario=self.user,
            linguagem=ProgressoPorLinguagem.LING_GOLANG,
            xp_total=50,
            nivel=1,
        )

    def test_login_required(self):
        response = self.client.get(reverse("painel_linguagens"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_painel_renderiza(self):
        self.client.login(username="pl", password="123")
        response = self.client.get(reverse("painel_linguagens"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Golang")


class CertificadoModelTests(TestCase):
    def test_criar_certificado(self):
        usuario = CustomUser.objects.create_user(username="cert", password="123")
        instrutor = CustomUser.objects.create_user(username="inst", password="123", is_instructor=True)
        curso = Course.objects.create(
            title="Curso",
            description="Desc",
            instructor=instrutor,
        )
        pdf = SimpleUploadedFile("certificado.pdf", b"arquivo")
        cert = Certificado.objects.create(
            usuario=usuario,
            curso=curso,
            codigo_validacao="ABC123",
            arquivo_pdf=pdf,
        )
        self.assertTrue(Certificado.objects.filter(id=cert.id).exists())

class EmitirCertificadoViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="ec", password="123")
        Avatar.objects.create(user=self.user)
        self.instrutor = CustomUser.objects.create_user(
            username="inst", password="123", is_instructor=True
        )
        self.curso = Course.objects.create(
            title="Curso", description="Desc", instructor=self.instrutor
        )
        self.lesson1 = Lesson.objects.create(
            course=self.curso, title="L1", video_url="http://example.com", order=1
        )
        self.lesson2 = Lesson.objects.create(
            course=self.curso, title="L2", video_url="http://example.com", order=2
        )

    def test_nao_concluido_redireciona(self):
        self.client.login(username="ec", password="123")
        response = self.client.get(reverse("emitir_certificado", args=[self.curso.id]))
        self.assertRedirects(response, reverse("mapa_mundi"))
        self.assertFalse(Certificado.objects.exists())

    def test_emite_certificado(self):
        self.client.login(username="ec", password="123")
        LessonProgress.objects.create(user=self.user, lesson=self.lesson1, completed=True)
        LessonProgress.objects.create(user=self.user, lesson=self.lesson2, completed=True)
        response = self.client.get(reverse("emitir_certificado", args=[self.curso.id]))
        cert = Certificado.objects.filter(usuario=self.user, curso=self.curso).first()
        self.assertIsNotNone(cert)
        self.assertRedirects(response, reverse("ver_certificado", args=[cert.id]))


class ValidarCertificadoViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="val", password="123")
        Avatar.objects.create(user=self.user)
        self.instrutor = CustomUser.objects.create_user(
            username="instv", password="123", is_instructor=True
        )
        self.curso = Course.objects.create(
            title="Curso Val", description="Desc", instructor=self.instrutor
        )
        pdf = SimpleUploadedFile("cert.pdf", b"arquivo")
        self.cert = Certificado.objects.create(
            usuario=self.user,
            curso=self.curso,
            codigo_validacao="VAL123",
            arquivo_pdf=pdf,
        )

    def test_certificado_valido(self):
        url = reverse("validar_certificado", args=[self.cert.codigo_validacao])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Certificado Válido")
        self.assertContains(response, self.curso.title)

    def test_certificado_invalido(self):
        url = reverse("validar_certificado", args=["XXXX"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Código Inválido")


class PerguntaDueloModelTests(TestCase):
    def test_create_pergunta_duelo_defaults(self):
        user1 = CustomUser.objects.create_user(username="u1", password="p1")
        user2 = CustomUser.objects.create_user(username="u2", password="p2")
        duelo = Duelo.objects.create(
            jogador_1=user1,
            jogador_2=user2,
            data_inicio=timezone.now(),
            data_fim=timezone.now(),
        )
        pergunta = PerguntaDuelo.objects.create(
            duelo=duelo,
            pergunta="Qual a capital?",
            resposta_correta="A",
        )

        self.assertFalse(pergunta.acertou_1)
        self.assertFalse(pergunta.acertou_2)
        self.assertEqual(str(pergunta), "Qual a capital?")

