from db import conn  # conn es psycopg2.connect()
import requests
from datetime import datetime
import pytz
import os

# --- Configuración ---
BOT_TOKEN = os.getenv("SECRET_BOT_TOKEN")  # export SECRET_BOT_TOKEN="..."

# Insertar una palabra en la tabla 'my_schema_1.dates_table'
def insert_word(word):
    cursor = conn.cursor()
    try:
        insert_query = """
            INSERT INTO my_schema_1.dates_table (word)
            VALUES (%s);
        """
        cursor.execute(insert_query, (word,))
        conn.commit()
        print(f"Palabra '{word}' insertada correctamente.")
    except Exception as e:
        print("Error al insertar la palabra:", e)
    finally:
        cursor.close()
        # NO cerramos conn aquí


# Contar filas de la tabla y retornar el número
def count_rows_dates_table():
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM my_schema_1.dates_table")
        count = cursor.fetchone()[0]
        return count
    except Exception as e:
        print("Error al contar filas:", e)
        return None
    finally:
        cursor.close()
        # NO cerramos conn aquí


# Enviar mensaje por Telegram
def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, data=payload)
    return response.json()

CHAT_ID = 1618347339 # reemplazar con tu chat ID real
arg_tz = pytz.timezone('America/Argentina/Buenos_Aires')


# Insertar palabra
insert_word("test")

# Contar filas
total_filas = count_rows_dates_table()

# Obtener hora actual en Argentina
hora_actual = datetime.now(arg_tz).strftime("%Y-%m-%d %H:%M:%S")

# Armar mensaje
mensaje = f"🕒 Hora: {hora_actual}\nTotal de filas: {total_filas}"

# Enviar mensaje
send_telegram_message(BOT_TOKEN, CHAT_ID, mensaje)

# Cerrar conexión al final
conn.close()
