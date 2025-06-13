from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from avatars.models import Avatar
from courses.models import Course, Lesson
from .models import Exercise


class CodeExecutorTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="dev", password="pw")
        Avatar.objects.create(user=self.user)
        course = Course.objects.create(
            title="Curso",
            description="d",
            instructor=self.user,
            linguagem=Course.LING_GOLANG,
        )
        lesson = Lesson.objects.create(
            course=course, title="L1", video_url="http://ex", order=1
        )
        self.exercise = Exercise.objects.create(
            lesson=lesson,
            question_text="Pergunta",
            correct_answer="ok\n",
            answer_type="code",
            xp_recompensa=5,
        )

    def test_requires_login(self):
        response = self.client.get(reverse("code_executor"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_execute_code_and_gain_xp(self):
        self.client.login(username="dev", password="pw")
        code = "print('ok')"
        response = self.client.post(
            reverse("code_executor") + f"?exercise_id={self.exercise.id}",
            {"code": code},
        )
        self.assertContains(response, "ok")
        avatar = Avatar.objects.get(user=self.user)
        self.assertEqual(avatar.xp_total, 5)

    def test_get_does_not_execute(self):
        self.client.login(username="dev", password="pw")
        self.client.get(
            reverse("code_executor") + f"?exercise_id={self.exercise.id}"
        )
        avatar = Avatar.objects.get(user=self.user)
        self.assertEqual(avatar.xp_total, 0)
