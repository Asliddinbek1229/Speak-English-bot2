import logging
from aiogram import Bot, Dispatcher, executor, types
from oxfordLookUp import getDefinitions
from googletrans import Translator

translator = Translator()

API_TOKEN = '6115928884:AAGMf2e9vkd5SbixuAXBmktA5NVPjQbkDes'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(f"👋 Assalomu alaykum <b>{message.from_user.first_name}</b>"
                        f"\n\n🤖 Speak English botiga xush kelibsiz"
                        f"\n\n♻️ Bu bot orqali siz👇👇👇\n"
                        f"👉 <i>Ingliz tilidagi istalgan so'zingizni ingliz tilidagi ma'nolarini topa olasiz</i>\n"
                        "👉 <i>Istalgan matningizni ingliz tiliga tarjima qila olasiz</i>"
                        f"\n\n⚙️ <b>Botga yana boshqa funksiyalar qo'shilmoqda...</b>")



@dp.message_handler()
async def echo(message: types.Message):
    lang = translator.detect(message.text).lang
    if len(message.text.split()) > 2:
        dest = 'uz' if lang=='en' else 'en'
        await message.reply(translator.translate(message.text, dest).text)

    else:
        if lang == 'en':
            word_id = message.text
        else:
            word_id = translator.translate(message.text, dest='en').text

        lookup = getDefinitions(word_id)
        if lookup:
            await message.reply(f"Word: {word_id} \nDefinitions:\n{lookup['definitions']}")
            if lookup['audio']:
                await message.reply(lookup['audio'])

        else:
            await message.reply(f"😕 Bunday so'z topilmadi!!!")




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)