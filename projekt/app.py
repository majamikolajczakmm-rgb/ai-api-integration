from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from google import genai  # TYLKO NOWY IMPORT
import os
import random
from dotenv import load_dotenv

load_dotenv()

# TEST: Sprawdzamy czy to ten plik
print(">>> TEST: URUCHOMIONO NOWY KOD (WERSJA GOOGLE-GENAI) <<<")

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# --- Nowa Konfiguracja (na rok 2026) ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("BŁĄD: Brak klucza w .env")
    client = None
else:
    # Nowy sposób tworzenia klienta
    client = genai.Client(api_key=GEMINI_API_KEY)
    print("Nowy klient Gemini (google-genai) gotowy!")

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/horoscope', methods=['POST'])
def get_horoscope():
    if not client: return jsonify({"error": "Brak klienta"}), 503
    try:
        data = request.get_json()
        zodiac = data.get('sign', 'Baran')
        
        # Nowa składnia: client.models.generate_content
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=f"Napisz krótki horoskop dla znaku {zodiac} po polsku."
        )
        return jsonify({"horoscope": response.text})
    except Exception as e:
        print(f"BŁĄD: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/tarot-card', methods=['POST'])
def get_tarot_card():
    if not client: return jsonify({"error": "Brak klienta"}), 503
    try:
        karty = ["Mag", "Głupiec", "Świat", "Słońce", "Księżyc", "Pustelnik"]
        wylosowana = random.choice(karty)
        
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=f"Zinterpretuj kartę tarota {wylosowana} jako kartę dnia po polsku."
        )
        return jsonify({
            "cardName": wylosowana,
            "interpretation": response.text
        })
    except Exception as e:
        print(f"BŁĄD: {e}")
        return jsonify({"error": str(e)}), 500

# Endpointy dla kompatybilności i charakterystyki (zaktualizowane)
@app.route('/api/kompatybilnosc', methods=['POST'])
def get_kompatybilnosc():
    data = request.get_json()
    s1, s2 = data.get('sign1'), data.get('sign2')
    response = client.models.generate_content(model='gemini-1.5-flash', contents=f"Kompatybilność {s1} i {s2} po polsku.")
    return jsonify({"compatibility": response.text})

@app.route('/api/znak-charakterystyka', methods=['POST'])
def get_znak_charakterystyka():
    data = request.get_json()
    zodiac = data.get('sign')
    response = client.models.generate_content(model='gemini-1.5-flash', contents=f"Charakterystyka znaku {zodiac} po polsku.")
    return jsonify({"charakterystyka": response.text})

if __name__ == '__main__':
    print("Serwer Gwiezdna Przystań startuje na porcie 5001...")
    app.run(debug=True, host='0.0.0.0', port=5001)