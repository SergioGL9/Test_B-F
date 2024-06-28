import io
import pandas as pd
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Token generado por BotFather.
API_TOKEN = '7409834731:AAEONDOqJmzLXeQ5Stn7Cqa1TdmlsdlPmyA'

# Creamos una instancia de la clase TeleBot utilizando el token generado.
bot = telebot.TeleBot(API_TOKEN)

# Generamos un DataFrame con los datos proporcionados en formato csv en un objeto llamado 'tiendas'.
# Este DataFrame contiene los datos de algunas de las tiendas de la compañía.
tiendas = pd.read_csv(io.StringIO('''
Tienda,CP,Dirección,Horarios
Condesa,"06170","Amsterdam EXT: 286, Cuauhtémoc, Ciudad de México, C.P. 06170",11:00-20:30
Universidad,"03100","Av. Universidad EXT: #749, Ciudad de México, Ciudad de México, C.P. 03100",11:00-20:30
Buenavista,"06350","Eje 1 EXT: Nte 259, Local PB, Cuauhtémoc, Ciudad de México, C.P. 06350",11:00-20:30
'''), dtype = {'CP':str}) # Le especificamos que la columna 'CP' se lea como texto y no como número, para evitar que elimine los ceros del inicio de los códigos.

# Comando de inicio
@bot.message_handler(commands=['start'])
def start(mensaje):
    respuesta = 'Bienvenidx, ¿en qué te puedo ayudar?'
    bot.reply_to(mensaje, respuesta)

# Comando para agendar una cita
@bot.message_handler(commands=['agendar'])
def agendar(mensaje):
    respuesta = 'Con el siguiente link puedes localizar tu sucursal más cercana y agendar una cita: https://www.benandfrank.com/stores'
    bot.reply_to(mensaje, respuesta)

# Comando para consultar las redes sociales de la compañía
@bot.message_handler(commands=['redes'])
def redes(mensaje):
    respuesta = "¡Síguenos en nuestras redes sociales!\nFacebook: https://www.facebook.com/benandfrank.mx\nX (antes Twitter): https://x.com/benandfrank_mx\nInstagram: https://www.instagram.com/benandfrank.mx/"
    bot.reply_to(mensaje, respuesta) 

# Comando de ayuda
@bot.message_handler(commands=['ayuda', 'help'])
def ayuda(mensaje):
    respuesta = 'Puedes usar los siguientes comandos:\n/start - Saludo de inicio\n/agendar - Para agendar una cita\n/sucursales - Para buscar una sucursal\n/redes - Para consultar nuestras redes sociales'
    bot.reply_to(mensaje, respuesta)
    
# Comando para buscar una sucursal
@bot.message_handler(commands=['sucursales'])
def sucursales(mensaje):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    for indice, sucursal in tiendas.iterrows():
        markup.add(KeyboardButton(f"{sucursal['Tienda']} - {sucursal['CP']}"))

    bot.send_message(mensaje.chat.id, "Seleccione la tienda por nombre o código postal:", reply_markup=markup)
    bot.register_next_step_handler(mensaje, enviar_info_sucursal)

def enviar_info_sucursal(mensaje):
    opc_seleccionada = mensaje.text.split(' - ')
    suc_nombre_o_cp = opc_seleccionada[0]
    suc_info = tiendas[(tiendas['Tienda'] == suc_nombre_o_cp) | (tiendas['CP'] == suc_nombre_o_cp)]
    
    if not suc_info.empty:
        for indice, sucursal in suc_info.iterrows():
            respuesta = f"Sucursal: {sucursal['Tienda']}\nDirección: {sucursal['Dirección']}\nHorarios: {sucursal['Horarios']}"
            bot.send_message(mensaje.chat.id, respuesta)
    else:
        bot.send_message(mensaje.chat.id, "No se encontró la tienda. Por favor, intenta de nuevo.")

# Inicia el bot
bot.polling()