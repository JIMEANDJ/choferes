import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
EXCEL_PATH = os.getenv("EXCEL_PATH", "Maestro de Clientes.xlsx")

if not TOKEN:
    raise ValueError("Falta la variable TOKEN en el archivo .env")
