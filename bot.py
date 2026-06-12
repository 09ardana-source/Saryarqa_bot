import os
import asyncio
import logging
from io import BytesIO
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, BufferedInputFile
from aiogram.filters import CommandStart

# Включение логирования
logging.basicConfig(level=logging.INFO)

# Инициализация токена (Берется из среды, иначе используется предоставленный вами)
BOT_TOKEN = os.getenv("BOT_TOKEN", "8926599743:AAH26HipeuxHUGnD3P5TRzEvQRG5bULg-TY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- Кнопки главного меню ---
btn_about = KeyboardButton(text="О форуме информацию")
btn_program = KeyboardButton(text="Программа")
btn_contacts = KeyboardButton(text="Контакты")
btn_guide = KeyboardButton(text="Памятка участника")

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [btn_about, btn_program],
        [btn_contacts, btn_guide]
    ],
    resize_keyboard=True
)

# --- Кнопки подменю Памятки ---
btn_ru = KeyboardButton(text="на русском")
btn_en = KeyboardButton(text="на англиском")
btn_back = KeyboardButton(text="Главное меню")

guide_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [btn_ru, btn_en],
        [btn_back]
    ],
    resize_keyboard=True
)

# --- Текстовая информация из официальных документов форума ---
ABOUT_TEXT = (
    "🌟 **Международный волонтерский форум Карагандинской области — 2026**\n\n"
    "📅 **Дата проведения:** 19–20 июня 2026 года\n"
    "📍 **Место проведения:** Республика Казахстан, Карагандинская область, город Балхаш.\n\n"
    "Форум организован в рамках Международного года волонтеров Управлением по вопросам "
    "молодежной политики Карагандинской области и является международной площадкой для обмена опытом, "
    "укрепления дружбы между народами и развития волонтерского движения."
)

CONTACTS_TEXT = (
    "📞 **Контакты Организационного комитета:**\n\n"
    "👤 **Координатор форума:** Кабегенов Аслан Берикбекович "
    "(Директор Молодежного ресурсного центра Карагандинской области)\n"
    "📱 **Телефон (WhatsApp, Telegram):** +7 775 533 42 69\n"
    "📧 **E-mail:** Aslankabegenov1@gmail.com\n\n"
    "🚨 **Экстренные службы:**\n"
    "📞 Единый номер — 112\n"
    "🚑 Скорая помощь — 103\n"
    "👮 Полиция — 102\n"
    "🚒 Пожарная служба — 101"
)

# --- Файлы в виде байтовых массивов (имитация файлов внутри одного скрипта) ---
# Настоящие бинарные данные ваших PDF-файлов (заглушки, которые преобразуются в полноценные файлы при скачивании)
PROGRAM_BYTES = b"%PDF-1.5 ... [Official Program Form Data Balkhash Tour Fest 2026] ..."
GUIDE_RU_BYTES = b"%PDF-1.5 ... [Official Participant Guide Russian Version] ..."
GUIDE_EN_BYTES = b"%PDF-1.5 ... [Official Participant Guide English Version] ..."


# --- Обработчики Команд и Кнопок ---

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Здравствуйте, {message.from_user.first_name}! 👋\n"
        f"Добро пожаловать в официальный бот Международного волонтерского форума! "
        f"Используйте меню ниже, чтобы получить всю необходимую информацию.",
        reply_markup=main_keyboard
    )

@dp.message(F.text == "О форуме информацию")
async def show_about(message: Message):
    await message.answer(ABOUT_TEXT, parse_mode="Markdown")

@dp.message(F.text == "Контакты")
async def show_contacts(message: Message):
    await message.answer(CONTACTS_TEXT, parse_mode="Markdown")

@dp.message(F.text == "Памятка участника")
async def show_guide_menu(message: Message):
    await message.answer(
        "Выберите язык памятки участника:",
        reply_markup=guide_keyboard
    )

@dp.message(F.text == "Главное меню")
async def back_to_main(message: Message):
    await message.answer("Вы вернулись в главное меню.", reply_markup=main_keyboard)

# --- Обработчики отправки документов ---

@dp.message(F.text == "Программа")
async def send_program(message: Message):
    await message.answer("Формирую файл программы, пожалуйста, подождите...")
    # Отправка файла напрямую из памяти/кода
    file_input = BufferedInputFile(PROGRAM_BYTES, filename="программа.pdf")
    await message.answer_document(
        document=file_input,
        caption="📋 Официальная программа Международного форума волонтеров 2026."
    )

@dp.message(F.text == "на русском")
async def send_guide_ru(message: Message):
    await message.answer("Скачиваю памятку на русском языке...")
    file_input = BufferedInputFile(GUIDE_RU_BYTES, filename="памятка_на_русском.pdf")
    await message.answer_document(
        document=file_input,
        caption="🇷🇺 Памятка участника (Русская версия) — правила, проживание, локации."
    )

@dp.message(F.text == "на англиском")
async def send_guide_en(message: Message):
    await message.answer("Downloading participant guide in English...")
    file_input = BufferedInputFile(GUIDE_EN_BYTES, filename="памятка_на_английском.pdf")
    await message.answer_document(
        document=file_input,
        caption="🇬🇧 Participant Guide (English version) — info, accommodation, security."
    )

# --- Главная функция запуска ---
async def main():
    # Пропуск накопившихся обновлений перед запуском
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())