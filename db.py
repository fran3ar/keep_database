import os
import psycopg2
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

DB_URL = os.getenv("DB_URL")

conn = psycopg2.connect(DB_URL)
