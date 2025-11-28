from db import conn  # conn es psycopg2.connect()
import requests
from datetime import datetime
import pytz
import os

#########################################
# ------- GEMINI NEWS GENERATION -------
#########################################

def generate_news():
    try:
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key=AIzaSyCRMtC-p086OkqPA3PNv_jboJdiwNBKAo8"

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": (
                                "Generate random news or interesting information about anything "
                                "so I can learn something new every day. Return only the information."
                            )
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 1.2,
                "maxOutputTokens": 150
            }
        }

        response = requests.post(url, json=payload)
        data = response.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"⚠️ Error al obtener noticia de Gemini: {e}"

#########################################
# ------------- TELEGRAM ---------------
#########################################

def send_telegram_message(token, chat_id, text):
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        response = requests.post(url, data=payload)
        return response.json()
    except Exception as e:
        print("⚠️ Error enviando mensaje a Telegram:", e)
        return None

#########################################
# ------------- DATABASE ----------------
#########################################

def insert_word(word):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO my_schema_1.dates_table (word) VALUES (%s);", (word,))
        conn.commit()
        cursor.close()
        return "OK"
    except Exception as e:
        return f"Error al insertar palabra: {e}"

def count_rows_dates_table():
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM my_schema_1.dates_table")
        count = cursor.fetchone()[0]
        cursor.close()
        return count
    except Exception as e:
        return f"Error al contar filas: {e}"

#########################################
# ------------ MAIN LOGIC --------------
#########################################

BOT_TOKEN = os.getenv("SECRET_BOT_TOKEN")
CHAT_ID = 1618347339
arg_tz = pytz.timezone("America/Argentina/Buenos_Aires")

# --- Intentar insertar palabra ---
insert_status = insert_word("test")

# --- Intentar contar filas ---
rows_count = count_rows_dates_table()

# --- Obtener noticia Gemini ---
news = generate_news()

# --- Hora actual ---
hora_actual = datetime.now(arg_tz).strftime("%Y-%m-%d %H:%M:%S")

# --- Construir mensaje principal ---
mensaje = (
    f"🕒 Hora: {hora_actual}\n"
    f"📥 Insertar palabra: {insert_status}\n"
    f"📊 Total filas: {rows_count}\n"
)

# --- Enviar mensajes SIEMPRE ---
send_telegram_message(BOT_TOKEN, CHAT_ID, mensaje)
send_telegram_message(BOT_TOKEN, CHAT_ID, news)

# --- Cerrar conexión (si existe) ---
try:
    conn.close()
except:
    pass