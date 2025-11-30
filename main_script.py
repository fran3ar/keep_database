from db import conn  # conn es psycopg2.connect()
import requests
from datetime import datetime
import pytz
import os
from groq import Groq
#########################################
# ------- GEMINI NEWS GENERATION -------
#########################################
GROQ_API_KEY_value = os.getenv("GROQ_API_KEY")
print(GROQ_API_KEY_value)

client = Groq(api_key = GROQ_API_KEY_value)

# Use .with_raw_response to access headers
response = client.chat.completions.with_raw_response.create(
    model="groq/compound-mini", # Assuming this is your valid model ID
    messages=[{"role": "user", "content": "Hello"}],
    temperature=1,
    max_completion_tokens=1024,
    stream=False # Headers are easier to read in non-streaming mode
)

# 1. Get the actual chat completion content
completion = response.parse()
print(f"Response: {completion.choices[0].message.content}")

# 2. Extract Rate Limit Headers (Your "Tier Usage")
headers = response.headers
print("\n--- API Key Tier Status ---")
print(f"Requests Remaining (RPM): {headers.get('x-ratelimit-remaining-requests')}")
print(f"Tokens Remaining (TPM): {headers.get('x-ratelimit-remaining-tokens')}")
print(f"Reset Time: {headers.get('x-ratelimit-reset-requests')}")
status = (
    "\n--- API Key Tier Status ---\n"
    f"Requests Remaining (RPM): {headers.get('x-ratelimit-remaining-requests')}\n"
    f"Tokens Remaining (TPM): {headers.get('x-ratelimit-remaining-tokens')}\n"
    f"Reset Time: {headers.get('x-ratelimit-reset-requests')}"
)

print(status)
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
news = status

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
