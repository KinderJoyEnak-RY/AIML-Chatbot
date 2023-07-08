import aiml
import re
from nltk.tokenize import word_tokenize
import random
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, BaseHandler
from helper.spell_checker import correction
from typing import Final
from helper.update_aiml import update_aiml_file


def chat():
    #update aiml file
    update_aiml_file()

# Inisialisasi kernel AIML
kernel = aiml.Kernel()
kernel.bootstrap(learnFiles="./data/std-startup.xml", commands="load aiml")

# Inisialisasi objek bot Telegram
TOKEN: Final = '6332106607:AAFwkVdcBAh9xKXhvO9DtTXqT6AyS3dAjzs'
BOT_USERNAME: Final = '@app123appbot'


#command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello selamat datang di Metopen Bot. ketikkan sesuatu mengenai Metopen!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('saya Metopen Bot! ketikkan sesuatu mengenai Metopen!')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('ini untuk custom command!')

# Pesan default jika tidak ada respons yang cocok
DEFAULT_RESPONSES = ["Maaf, saya tidak dapat memahami pertanyaan Anda. Mohon sertakan konteks/informasi dasar pada pertanyaan Anda."]

# Fungsi untuk mendapatkan respons dari AIML kernel
def get_bot_response(query: str) -> str:
    # Mengecek pola yang dikecualikan dari pengecekan ejaan
    excluded_patterns = ['nama ', 'nama saya ', 'aku', 'saya']
    if any(query.startswith(pattern) for pattern in excluded_patterns):
        words = query.split()
        correction_sentence = query
    else:
        # Case folding
        query = query.lower()
        query = re.sub(r'[^\w\s]', '', query)
        print('After case folding:', query)

        # Tokenisasi
        words = word_tokenize(query)
        print('After tokenizing:', words)

        # Koreksi ejaan
        words = [correction(w) for w in words]
        correction_sentence = " ".join(words)
        print('After spell correction:', correction_sentence)
        print('Pattern : ', correction_sentence)

    # Panggil kernel AIML
    response = kernel.respond(correction_sentence)
    x = response.replace("((", "<").replace("))", ">")
    x = x.replace("</br>", "\n")
    print('Bot Response:', x)
    if not x or x == '':
        return random.choice(DEFAULT_RESPONSES)
    return x


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    query: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{query}"')

    if message_type == 'group':
        if BOT_USERNAME in query:
            new_text: str = query.replace(BOT_USERNAME, '').strip()
            response: str = get_bot_response(new_text)
        else:
            return
    else:
        response: str = get_bot_response(query)

    await update.message.reply_text(response)


class ErrorHandler(BaseHandler):
    def __init__(self):
        super().__init__(filters.UpdateFilter())

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logging.error(f"Update {update} caused error {context.error}")
    
    def check_update(self, update: Update) -> bool:
        return True



if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    print('Starting Bot..')
    app = Application.builder().token(TOKEN).build()

    #command
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    #message
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #errors
    app.add_handler(ErrorHandler())

    #polls the bot
    print('Polling...')
    app.run_polling()