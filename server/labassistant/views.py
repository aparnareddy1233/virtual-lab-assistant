import os
import json
import random
import requests
import markdown
from dotenv import load_dotenv
from googletrans import Translator
import fitz  # PyMuPDF

from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY") or "YOUR_API_KEY_HERE"
API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}'

translator = Translator()

LANGUAGES = {
    "en": "English", "hi": "Hindi", "te": "Telugu", "ta": "Tamil", "kn": "Kannada",
    "ml": "Malayalam", "mr": "Marathi", "gu": "Gujarati", "pa": "Punjabi",
    "bn": "Bengali", "ur": "Urdu", "zh-cn": "Chinese", "ja": "Japanese",
    "de": "German", "fr": "French", "es": "Spanish", "ru": "Russian", "it": "Italian"
}

def send_message(prompt):
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(API_URL, json=data, timeout=15)
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except requests.exceptions.Timeout:
        return "❌ Request timed out. Please check your internet connection or try again."
    except requests.exceptions.RequestException as e:
        return f"❌ Failed to connect to Gemini API: {e}"
    except (KeyError, IndexError, TypeError):
        return "⚠️ Gemini response parsing error."

def build_prompt(user_prompt, text=None):
    reference = f"Reference:\n{text[:6000]}\n\n" if text else ""
    return f"{reference}Q: {user_prompt}"

@login_required(login_url='login')
def index(request):
    response, tts_text, user_language = None, "", "en"

    if request.method == 'POST':
        uploaded_file = request.FILES.get('datafile')
        user_prompt = request.POST.get('user_prompt', '').strip()
        selected_lang = request.POST.get('selected_lang', 'en')
        user_language = selected_lang

        if not user_prompt:
            messages.error(request, "❗ Please enter a question.")
            return redirect('index')

        try:
            detected_lang = translator.detect(user_prompt).lang
            translated_prompt = translator.translate(user_prompt, src=detected_lang, dest='en').text
        except Exception as e:
            translated_prompt = user_prompt
            messages.warning(request, f"🌐 Translation issue: {e}")

        file_text = ""
        if uploaded_file and uploaded_file.name.endswith('.pdf'):
            try:
                file_path = default_storage.save(uploaded_file.name, uploaded_file)
                with default_storage.open(file_path, 'rb') as f:
                    pdf = fitz.open(stream=f.read(), filetype="pdf")
                    for page in pdf:
                        file_text += page.get_text()
            except Exception as e:
                messages.error(request, f"📄 PDF parsing failed: {e}")

        prompt = build_prompt(translated_prompt, file_text)
        english_response = send_message(prompt)

        if not english_response or "⚠️" in english_response or "❌" in english_response:
            messages.error(request, f"🤖 Gemini Error: {english_response}")
            return redirect('index')

        try:
            translated_response = translator.translate(english_response, src='en', dest=selected_lang).text
        except Exception as e:
            translated_response = english_response
            messages.warning(request, f"🌐 Translation failed: {e}")

        response = markdown.markdown(translated_response)
        tts_text = translated_response

    return render(request, 'index.html', {
        'response': response,
        'tts_text': tts_text,
        'selected_lang': user_language,
        'languages': LANGUAGES
    })

def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
        if user:
            login(request, user)
            return redirect('index')
        messages.error(request, "Invalid username or password")
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if not username or not password:
            messages.error(request, "All fields are required")
        elif password != confirm:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, "Account created. Please login.")
            return redirect('login')

    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@csrf_exempt
def chemical_reaction_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            chemicals = data.get('chemicals', [])
            if len(chemicals) < 2:
                return JsonResponse({'error': 'Minimum two chemicals required'}, status=400)
            result = simulate_reaction(chemicals)
            return JsonResponse({'result': result})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def simulate_reaction(chemicals):
    outcomes = [
        f"{chemicals[0]} and {chemicals[1]} produced a vibrant color change.",
        f"{chemicals[0]} and {chemicals[1]} released gas bubbles.",
        f"{chemicals[0]} and {chemicals[1]} formed a precipitate.",
        f"{chemicals[0]} and {chemicals[1]} caused a temperature spike."
    ]
    return random.choice(outcomes)

def explain_reaction(chemicals):
    prompt = f"Explain the reaction between: {', '.join(chemicals)}. Include reaction type, steps, and safety precautions."
    return send_message(prompt)

def animate_reaction(result):
    animations = {
        'color change': 'animateColorChange()',
        'gas bubbles': 'animateGasBubbles()',
        'precipitate': 'animatePrecipitate()',
        'temperature spike': 'animateTemperatureSpike()'
    }
    for key in animations:
        if key in result:
            return animations[key]
    return 'defaultAnimation()'

@login_required
def chemical_lab(request):
    return render(request, 'chemical.html')
