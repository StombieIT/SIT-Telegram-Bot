from config import *
@bot.message_handler(commands=["start"])
def start(message):
	bot.reply_to(message,
		'Воспользуйтесь прикреплённой ниже клавиатурой\
		или введите "/" в поле с текстом сообщения для того,\
		чтобы посмотреть список команд с описанием.',
	reply_markup=keyboard_main)
@bot.message_handler(commands=["password"])
def password(message):
	bot.reply_to(message, "Укажите необходимое количество символов, не превышающее 128.")
	bot.register_next_step_handler(message, password_generate)
def password_generate(message):
	if str(type(message.text)) == "<class 'str'>":
		password = ""
		try:
			int(message.text)
		except ValueError:
			bot.reply_to(message, "Обнаружены посторонние символы 🙈.")
		else:
			if int(message.text) > 0:
				if int(message.text) <= 128:
					for i in range(int(message.text)):
						if (i % 5 == 0) and (i != 0):
							password += choice(list("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"))
						elif i % 2 == 0:
							password += choice(list("qwrtpsdfghjklzxcvbnmQWRTPSDFGHJKLZXCVBNM"))
						elif i % 3 == 0:
							password += choice(list("0123456789"))
						else:
							password += choice(list("eyuioaEYUIOA"))
					bot.send_message(message.chat.id, "Готово:")
					bot.send_message(message.chat.id, password)
				else:
					bot.reply_to(message, 'Превышено максимальное допустимое количество символов 🙈.')
			else:
				bot.reply_to(message, "Некорректно указано количество символов 🙈.")
	else:
		bot.reply_to(message, 'Обнаружен некорректный формат сообщения 🙈.')
@bot.message_handler(commands=['weather'])
def weather(message):
	bot.reply_to(message, 'Укажите населённый пункт.')
	bot.register_next_step_handler(message, weather_choose_city)
def weather_choose_city(message):
	if str(type(message.text)) == "<class 'str'>":
		city = message.text
		try:
			observation = owm.weather_at_place(city)
		except pyowm.exceptions.api_response_error.NotFoundError:
			bot.reply_to(message, 'Не могу найти указанный населённый пункт 🙈.')
		else:
			weather = observation.get_weather()
			status = weather.get_status()
			temperature = weather.get_temperature('celsius')['temp']
			wind = weather.get_wind('meters_sec')['speed']
			humidity = weather.get_humidity()
			if status == 'Clouds':
				status = 'облачно'
			elif status == 'Clear':
				status = 'ясно'
			elif status == 'Rain':
				status = 'идёт дождь'
			elif status == 'Snow':
				status = 'идёт снег'
			bot.send_message(message.chat.id,
				'Погода в {c}:\
				\nСейчас {s}.\
				\nТемпература составляет {t} °C.\
				\nСкорость ветра составляет {w} м/с.\
				\nВлажность воздуха составляет {h} %.'.format(c=city, s=status, t=temperature, w=wind, h=humidity)
			)
	else:
		bot.reply_to(message, 'Обнаружен некорректный формат сообщения 🙈.')
@bot.message_handler(commands=['qr'])
def qr(message):
	bot.reply_to(message, 'Укажите действие.', reply_markup=keyboard_qr)
	bot.register_next_step_handler(message, qr_choice)
def qr_choice(message):
	if str(type(message.text)) == "<class 'str'>":
		if message.text == 'Сгенерировать':
			bot.send_message(message.chat.id, 'Укажите текст, содержащий не более 256 символов.')
			bot.register_next_step_handler(message, qr_generate)
		elif message.text == 'Считать':
			bot.send_message(message.chat.id, 'Прикрепите изображение с QR кодом.')
			bot.register_next_step_handler(message, qr_read)
		else:
			bot.reply_to(message, 'Некорректно указано действие 🙈.')
	else:
		bot.reply_to(message, 'Обнаружен некорректный формат сообщения 🙈.')
def qr_generate(message):
	if str(type(message.text)) == "<class 'str'>":
		if len(message.text) <= 256:
			image = make(message.text)
			image.save('qr_generate.png')
			byte = open('qr_generate.png', 'rb')
			bot.send_message(message.chat.id, 'Готово:')
			bot.send_photo(message.chat.id, byte)
			byte.close()
			remove('qr_generate.png')
		else:
			bot.reply_to(message, 'Превышено максимальное допустимое количество символов 🙈.')
	else:
		bot.reply_to(message, 'Обнаружен некорректный формат сообщения 🙈.')
def qr_read(message):
	if str(type(message.photo)) == "<class 'list'>":
		info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
		byte = bot.download_file(info.file_path)
		with open('qr_read.png', 'wb') as image:
			image.write(byte)
		image = imread('qr_read.png')
		barcodes = decode(image)
		for barcode in barcodes:
			barcodeData = barcode.data.decode('utf-8')
		try:
			type(barcodeData)
		except UnboundLocalError:
			bot.reply_to(message, 'Не удалось распознать QR код 🙈.')
		else:
			bot.send_message(message.chat.id, 'Готово:')
			bot.send_message(message.chat.id, barcodeData)
		remove('qr_read.png')
	else:
		bot.reply_to(message, 'Обнаружен некорректный формат сообщения 🙈.')
@bot.message_handler(commands=['calculate'])
def calculate(message):
	bot.reply_to(message,
		'Укажите математическое действие, используя следующие операторы:\
		\n{ - } - разница,\
		\n{ + } - сумма,\
		\n{ * } - произведение,\
		\n{ / } - частное,\
		\n{ // } - частное без остатка,\
		\n{ % } - остаток от частного,\
		\n{ ** } - возведение в степень,\
		\n{ () } - приоритет действий.'
	)
	bot.register_next_step_handler(message, calculate_count)
def calculate_count(message):
	if str(type(message.text)) == "<class 'str'>":
		try:
			result = eval(message.text)
		except NameError:
			bot.reply_to(message, "Обнаружены посторонние символы 🙈.")
		except SyntaxError:
			bot.reply_to(message, "Обнаружены посторонние символы 🙈.")
		else:
			bot.send_message(message.chat.id, 'Готово:')
			bot.send_message(message.chat.id, result)
	else:
		bot.reply_to(message, 'Обнаружен некорректный формат сообщения 🙈.')
@bot.message_handler(commands=['do'])
def do(message):
	if message.chat.id in ADMIN:
		bot.reply_to(message, 'Укажите действие.')
		bot.register_next_step_handler(message, do_exec)
	else:
		bot.send_message(message.chat.id,
		'Не понял 😕. Воспользуйтесь прикреплённой ниже клавиатурой\
		или введите "/" в поле с текстом сообщения для того,\
		чтобы посмотреть список команд с описанием.'
		)
def do_exec(message):
	if str(type(message.text)) == "<class 'str'>":
		try:
			exec(message.text)
		except SyntaxError:
			bot.reply_to(message, 'Обнаружена синтаксическая ошибка 🙈.')
		except NameError:
			bot.reply_to(message, 'Обнаружена синтаксическая ошибка 🙈.')
		else:
			bot.send_message(message.chat.id, 'Выполнено.')
	else:
		bot.reply_to(message, 'Обнаружен некорректный формат сообщения 🙈.')
@bot.message_handler(content_types=["text"])
def main(message):
	bot.send_message(message.chat.id,
		'Не понял 😕. Воспользуйтесь прикреплённой ниже клавиатурой\
		или введите "/" в поле с текстом сообщения для того,\
		чтобы посмотреть список команд с описанием.'
		)
if __name__ == '__main__':
	bot.polling()
