# exercises/views.py
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import io
import sys

@csrf_exempt
def code_executor(request):
    output = ""
    code = ""

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

    return render(request, "exercises/code_executor.html", {"output": output, "code": code})
