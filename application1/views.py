from django.shortcuts import render
from gtts import gTTS
import os
from application1 import views
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import speech_recognition as sr
import tempfile
import os

def home(request):
    return render(request, "application1/home.html")

def Test_Case1(request):
    audio_file=None
    if request.method=="POST":
        text=request.POST.get("text")
        if text:
            tts=gTTS(text=text,lang="en",slow=False)
            os.makedirs("media",exist_ok=True)
            audio_file="media/output.mp3"
            tts.save(audio_file)
    return render(request,"application1/S1.html",{"audio_file":audio_file})


from pydub import AudioSegment

def Test_Case2(request):
    if request.method == "POST" and request.FILES.get("audio"):
        audio_file = request.FILES["audio"]

        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            for chunk in audio_file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        
        fixed_path = tmp_path.replace(".wav", "_fixed.wav")
        try:
            sound = AudioSegment.from_file(tmp_path)
            sound.export(fixed_path, format="wav")
        except Exception as e:
            return JsonResponse({"error": f"Audio conversion failed: {e}"}, status=500)

        recognizer = sr.Recognizer()
        text = ""

        try:
            with sr.AudioFile(fixed_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language="en-US")
        except sr.UnknownValueError:
            text = "⚠️ Could not understand audio"
        except sr.RequestError as e:
            text = f"⚠️ Could not request results; {e}"
        except Exception as e:
            text = f"⚠️ Processing error: {e}"
        os.remove(tmp_path)
        os.remove(fixed_path)

        return JsonResponse({"text": text})

    return JsonResponse({"error": "No audio file received"}, status=400)
