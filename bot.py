import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import openpyxl
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from config import TOKEN, EXCEL_PATH

def cargar_clientes():
    wb = openpyxl.load_workbook(EXCEL_PATH)
    ws = wb.active
    por_codigo = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        distribuidora, codigo, nombre, ruta, coord_x, coord_y = row
        if ruta is None:
            continue
        lat = coord_y / 1e7
        lon = coord_x / 1e7
        por_codigo[int(codigo)] = {
            "codigo": int(codigo),
            "nombre": nombre,
            "distribuidora": distribuidora,
            "ruta": int(ruta),
            "maps": f"https://www.google.com/maps?q={lat},{lon}",
        }
    return por_codigo

POR_CODIGO = cargar_clientes()

async def start(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bienvenido al bot de rutas Coca-Cola.\n\n"
        "Escribe el *código del cliente* y te mostraré su nombre y ubicación en Google Maps.",
        parse_mode="Markdown"
    )

async def buscar(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()

    if not texto.isdigit():
        await update.message.reply_text("Por favor escribe solo el código numérico del cliente.")
        return

    codigo = int(texto)

    if codigo not in POR_CODIGO:
        await update.message.reply_text(f"No se encontró ningún cliente con el código *{codigo}*.", parse_mode="Markdown")
        return

    c = POR_CODIGO[codigo]
    await update.message.reply_text(
        f"*{c['nombre']}*\n"
        f"Código: `{c['codigo']}`\n"
        f"Distribuidora: {c['distribuidora']}\n"
        f"Ruta: {c['ruta']}\n"
        f"{c['maps']}",
        parse_mode="Markdown"
    )

def _iniciar_http():
    class HealthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")
        def log_message(self, *args):
            pass
    puerto = int(os.getenv("PORT", "10000"))
    HTTPServer(("0.0.0.0", puerto), HealthHandler).serve_forever()

def main():
    threading.Thread(target=_iniciar_http, daemon=True).start()
    print("Cargando clientes desde Excel...")
    print(f"Total clientes cargados: {len(POR_CODIGO)}")
    print("Bot iniciado. Presiona Ctrl+C para detener.")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buscar))
    app.run_polling()

if __name__ == "__main__":
    main()
