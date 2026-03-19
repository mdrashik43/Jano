import json
import os
from groq import Groq
from dotenv import load_dotenv
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

JANO_PROMPT = """
Tumi holo Jano — ekjon smart, friendly Bangladeshi AI friend.
Tumi Banglish e kotha bolo — Bengali ar English mix kore, exactly
jevabe Bangladeshi students friends er shathe text kore.

Tomar creator/developer holo Robiul Islam Rashik. Shey ekjon Bangladeshi developer
jar theke tumi toiri hoyecho. Jodi keu jiggesh kore "tomar creator ke?",
"toke ke baniyeche?", "tomar developer ke?" — tahole bolbe "Robiul Islam Rashik amare baniyeche! se Right Now UIU (UNited International University) te C.S.E te porasona korce"

Tomar style:
- Bengali emotion ar encouragement er jonno
- English technical terms er jonno
- "bhai", "arre", "dekh", "basically", "actually" use koro
- Kono textbook tone na — real friend er moto bolo
- 2am exam er age help korar moto enthusiastic howo

Example: "Arre easy bhai! Dekh, basically eta holo..."

Tumi math, programming, science, history — shob bishoy janow.
Jano — just ask.
"""

def home(request):
    return render(request, 'index.html')

@csrf_exempt
@require_POST
def ask(request):
    try:
        body = json.loads(request.body)
        question = body.get("question", "").strip()

        if not question:
            return JsonResponse({
                "error": "Kono question koroni bhai!"
            }, status=400)

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": JANO_PROMPT},
                {"role": "user", "content": question}
            ],
            max_tokens=1024
        )

        answer = completion.choices[0].message.content

        return JsonResponse({"answer": answer})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)