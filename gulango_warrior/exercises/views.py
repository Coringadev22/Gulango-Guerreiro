# exercises/views.py
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import io
import sys

from avatars.models import Avatar
from .models import Exercise

@csrf_exempt
@login_required
def code_executor(request):
    output = ""
    code = ""
    xp_message = None

    exercise_id = request.GET.get("exercise_id") or request.POST.get("exercise_id")
    exercise = None
    if exercise_id:
        exercise = get_object_or_404(Exercise, pk=exercise_id)

    if request.method == "POST":
        code = request.POST.get("code", "")
        buffer = io.StringIO()
        try:
            sys.stdout = buffer
            exec(code, {})  # NUNCA use isso em produção sem sandbox!
            output = buffer.getvalue()
        except Exception as e:
            output = str(e)
        finally:
            sys.stdout = sys.__stdout__

        if exercise and output.strip() == exercise.correct_answer.strip():
            avatar = Avatar.objects.get(user=request.user)
            avatar.ganhar_xp(exercise.xp_recompensa)
            xp_message = f"Voc\u00ea ganhou {exercise.xp_recompensa} XP!"

    context = {
        "output": output,
        "code": code,
        "exercise": exercise,
        "xp_message": xp_message,
    }
    return render(request, "exercises/code_executor.html", context)
