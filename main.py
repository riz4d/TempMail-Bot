# copyright 2020-21 @Mohamed Rizad
# Telegram @riz4d
# Instagram @riz.4d
import telebot
import requests
from telebot.types import InlineKeyboardButton

# Fillout Here The BotToken it gets from botfather further queries @riz4d 0n telegram
bot = telebot.TeleBot('5219959835:AAFt3APRmPLcsxdzV7vtUdhqdFr54QrPn_s')

while True:
    try:

        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(InlineKeyboardButton(text='Generate email'))
        keyboard.add(InlineKeyboardButton(text='Refresh inbox'))
        keyboard.add(InlineKeyboardButton(text='About'))


        @bot.message_handler(commands=['start'])
        def start_message(message):
            bot.send_message(message.chat.id,
                             'Hey User., Welcome to MysteryMail Bot \nUsage:_\nTo Generate emails by clicking on the button "Generate email"\nTo refresh your inbox click on the button "Refresh inbox". After a new letter arrives, you will see a button with a subject line, click on this button to read the message. \n\n Dev : @riz4d',
                             reply_markup=keyboard)


        @bot.message_handler(content_types=['text'])
        def send_text(message):
            if message.text.lower() == 'generate email':
                email = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1").json()[0]
                ekeyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                ekeyboard.add(InlineKeyboardButton(text='Generate email'))
                ekeyboard.add(InlineKeyboardButton(text='Refresh inbox\n[' + str(email) + "]"))
                ekeyboard.add(InlineKeyboardButton(text='About'))
                bot.send_message(message.chat.id, "Your Temporary E-mail:")
                bot.send_message(message.chat.id, str(email), reply_markup=ekeyboard)
            elif message.text.lower() == 'refresh inbox':
                bot.send_message(message.chat.id, 'First, generate an email', reply_markup=keyboard)
            elif message.text.lower() == 'about':
                bot.send_message(message.chat.id,
                                 'What is Mystery Mail?\n- it is a free email service that allows to receive email at a temporary address that self-destructed after a certain time elapses. It is also known by names like tempmail, 10minutemail, 10minmail, throwaway email, fake-mail , fake email generator, burner mail or trash-mail\n\nHow Mystery Mail Become Safer You?\n- Using the temporary mail allows you to completely protect your real mailbox against the loss of personal information. Your temporary e-mail address is completely anonymous. Your details: information about your person and users with whom you communicate, IP-address, e-mail address are protected and completely confidential.\n\n➪ Bot Name : MysteryMail\n➪ Author : @riz4d\n➪ Language : Python \n➪ Donate : https://www.paypal.com/paypalme/rizadx96')
            elif message.text.lower()[14] == "[":
                email = message.text.lower()[15:message.text.lower().find("]")]
                bkeyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                bkeyboard.add(InlineKeyboardButton(text='Refresh inbox\n[' + str(email) + "]"))
                bkeyboard.add(InlineKeyboardButton(text='Generate email'))
                try:
                    data = requests.get(
                        "https://www.1secmail.com/api/v1/?action=getMessages&login=" + email[:email.find(
                            "@")] + "&domain=" + email[email.find("@") + 1:]).json()
                    if 'id' in data[0]:
                        for i in range(len(data)):
                            id = data[i]['id']
                            subject = data[i]['subject']
                            fromm = data[i]['from']
                            date = data[i]['date']
                            if len(subject) > 15:
                                subject = str(subject[0:15]) + "..."
                            bkeyboard.add(InlineKeyboardButton(
                                text=str(subject) + "\n from: " + fromm + " in " + "[id" + str(id) + "][" + str(
                                    email) + "]"))
                            bot.send_message(message.chat.id,
                                             "Subject: " + subject + "\n From: " + fromm + "\n Date:" + date,
                                             reply_markup=bkeyboard)
                            count = i + 1
                        bot.send_message(message.chat.id, "Here " + str(
                            count) + " message we're found\nClick on the below button to read the message\n\n Further Queries @riz4d")
                    else:
                        bot.send_message(message.chat.id, 'Nothing found', reply_markup=bkeyboard)
                except BaseException:
                    bot.send_message(message.chat.id, 'No messages were received...', reply_markup=bkeyboard)
            elif message.text.lower().find("[id"):
                try:
                    data = message.text.lower()[message.text.lower().find("[id"):]
                    id = data[data.find("[") + 3:data.find(']')]
                    email = data[data.find("][") + 2:-1]
                    msg = requests.get("https://www.1secmail.com/api/v1/?action=readMessage&login=" + email[:email.find(
                        "@")] + "&domain=" + email[email.find("@") + 1:] + "&id=" + id).json()
                    bot.send_message(message.chat.id,
                                     'Message ✉️\n\n   From: ' + msg['from'] + "\n   Subject: " + msg[
                                         'subject'] + "\n   Date: " + msg[
                                         'date'] + "\n   text: " + msg['textBody'])
                except BaseException:
                    pass


        bot.polling(none_stop=True, interval=1, timeout=5000)
    except BaseException:
        pass
        
# Stay tuned for more : Instagram @riz.4d
