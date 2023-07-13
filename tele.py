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
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import string


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

# membuat stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Mendefinisikan path ke file kamus kata dasar
kamus_path = 'helper/kata-dasar.txt'

# Memuat kamus kata dasar dari file
with open(kamus_path, 'r') as file:
    kamus_kata_dasar = file.read().splitlines()

# Fungsi untuk mendapatkan respons dari AIML kernel
def get_bot_response(query: str) -> str:
    # Preprocessing
    preprocessed_query = preprocess(query)

    # Call AIML kernel
    response = kernel.respond(preprocessed_query)
    x = response.replace("((", "<").replace("))", ">").replace("]", "").replace("'", "")
    print('Bot Response = ', x)
    if x is None or x == '':
        return random.choice(DEFAULT_RESPONSES)
    return x

def preprocess(text):
    # melakukan case folding
    text = text.lower()
   
    # menghilangkan nomor dan tanda baca
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
   
    # melakukan tokenizing
    words = text.split()
   
    # melakukan spell check
    corrected_words = []
    for word in words:
        corrected_words.append(correction(word))

    # melakukan stemming dengan kamus kata dasar
    stemmed_words = []
    for word in corrected_words:
        if word in kamus_kata_dasar:
            stemmed_words.append(word)
        else:
            stemmed_words.append(stemmer.stem(word))
       
    # melakukan filtering stopwords
    with open('helper/data-stopword.txt', 'r') as file:
        stopwords = file.read().splitlines()
    filtered_words = [word for word in stemmed_words if word not in stopwords]
   
    print("Hasil case folding: ", text)
    print("Hasil penghilangan nomor dan tanda baca: ", text)
    print("Hasil tokenizing: ", words)
    print("Hasil koreksi : ", corrected_words)
    print("Hasil stemming: ", stemmed_words)
    print("Hasil filtering stopwords: ", filtered_words)
    
    # menggabungkan kata yang telah dilakukan preprocessing
    preprocessed_text = ' '.join(filtered_words)

    print("Pattern :",preprocessed_text)
    return preprocessed_text


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