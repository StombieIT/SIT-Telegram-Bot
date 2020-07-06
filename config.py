import pyowm
from telebot import TeleBot
from database import DataBase
from telebot.types import ReplyKeyboardMarkup
from qrcode import make
from cv2 import imread
from os import remove
from pyzbar.pyzbar import decode
from random import choice
#OWM
owm = pyowm.OWM(API_key='', language = 'ru')
#Bot
bot = TeleBot("")
#DataBase
db = DataBase('logs.db')
db.create()
#Keyboards
keyboard_main = ReplyKeyboardMarkup(True)
keyboard_main.row('/password', '/weather', '/qr', '/calculate')
keyboard_translit_language = ReplyKeyboardMarkup(True, True)
keyboard_translit_language.row("Русский", "English")
keyboard_qr = ReplyKeyboardMarkup(True, True)
keyboard_qr.row("Сгенерировать", "Считать")
#ADMIN
ADMIN = []
