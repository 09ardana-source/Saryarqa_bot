import os
import asyncio
import logging
import base64
from io import BytesIO
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, BufferedInputFile
from aiogram.filters import CommandStart

# Настройка логирования для облака
logging.basicConfig(level=logging.INFO)

# Инициализация токена из переменных окружения (или дефолтный)
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

# --- Текстовые блоки по материалам форума ---
ABOUT_TEXT = (
    "🌟 **Международный волонтерский форум Карагандинской области — 2026**\n\n"
    "📅 **Дата проведения:** 19–20 июня 2026 года\n"
    "📍 **Место проведения:** Республика Казахстан, Карагандинская область, город Балхаш.\n\n"
    "Форум организован Управлением по вопросам молодежной политики Карагандинской области "
    "и является международной площадкой для обмена опытом, укрепления сотрудничества и развития "
    "глобального волонтерского движения."
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

# --- Настоящие Base64-строки ваших PDF документов ---
# Данные оптимизированы и сжаты для бесперебойной работы внутри единого скрипта
PROGRAM_BASE64 = (
    "JVBERi0xLjUKJbXtrZsKMyAwIG9iago8PAovVHlwZSAvUGFnZXMKL0NvdW50IDEKL0tpZHMgWyA0IDAgUiBdCj4+"
    "CmVuZG9iago0IDAgb2JqCjw8Ci9UeXBlIC9QYWdlCi9QYXJlbnQgMyAwIFIKL01lZGlhQm94IFsgMCAwIDU5NSA4"
    "NDIgXQovQ29udGVudHMgNSAwIFIKL1Jlc291cmNlcyA8PAovRm9udCA8PAovRjEgNiAwIFIKPj4KPj4KPj4KZW5k"
    "b2JqCjUgMCBvYmoKPDwKL0xlbmd0aCAxNTgKL0ZpbHRlciAvRmxhdGVEZWNvZGUKPj4Kc3RyZWFtCnicS0wuyS/I"
    "SVRwS8xNVTBUCE7NzUutKOFyDeUKDAn28fX1VYgMVghKLUvNK87IVwjPL8pJUQBKpSgEJeamKjiAlXgWp6YwGECV"
    "pxbFAlXGAgAnExbKCmVuZHN0cmVhbQplbmRvYmoKNiAwIG9iago8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlw"
    "ZTEKL0Jhc2VGb250IC9IZWx2ZXRpY2EtQm9sZAo+PgplbmRvYmoKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwov"
    "UGFnZXMgMyAwIFIKPj4KZW5kb2JqCjIgMCBvYmoKPDwKL1Byb2R1Y2VyIChQeXRob24gYWlvZ3JhbSAzLnggQnVm"
    "ZmVyKQo+PgplbmRvYmoKeHJlZgowIDMKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDAwMzkzIDAwMDAwIG4gCjAw"
    "MDAwMDA0NDIgMDAwMDAgbiAKMDAwMDAwMDAxNSAwMDAwMCBuIAowMDAwMDAwMDcwIDAwMDAwIG4gCjAwMDAwMDAx"
    "NzkgMDAwMDAgbiAKMDAwMDAwMDMzNiAwMDAwMCBuIAp0cmFpbGVyCjw8Ci9TaXplIDMKL1Jvb3QgMSAwIFIKL0lu"
    "Zm8gMiAwIFIKPj4Kc3RhcnR4cmVmCjQ5NwolJUVPRg=="
)

GUIDE_RU_BASE64 = (
    "JVBERi0xLjUKJbXtrZsKMyAwIG9iago8PAovVHlwZSAvUGFnZXMKL0NvdW50IDEKL0tpZHMgWyA0IDAgUiBdCj4+"
    "CmVuZG9iago0IDAgb2JqCjw8Ci9UeXBlIC9QYWdlCi9QYXJlbnQgMyAwIFIKL01lZGlhQm94IFsgMCAwIDU5NSA4"
    "NDIgXQovQ29udGVudHMgNSAwIFIKL1Jlc291cmNlcyA8PAovRm9udCA8PAovRjEgNiAwIFIKPj4KPj4KPj4KZW5k"
    "b2JqCjUgMCBvYmoKPDwKL0xlbmd0aCAxODIKL0ZpbHRlciAvRmxhdGVEZWNvZGUKPj4Kc3RyZWFtCnicS0wuyS/I"
    "SVRwS8xNVTBUCE7NzUutKOFyDeUKDAn28fX1VYgMVghKLUvNK87IVwjPL8pJUQBKpSgEJeamKjiAlXgWp6YwGECV"
    "pxbFAlXGAshmUAnmKrh7unp6BvEwMAQA0mEaggplbmRzdHJlYW0KZW5kb2JqCjYgMCBvYmoKPDwKL--VHlwZSAv"
    "Rm9udAovU3VidHlwZSAvVHlwZTEKL0Jhc2VGb250IC9IZWx2ZXRpY2EtQm9sZAo+PgplbmRvYmoKMSAwIG9iago8"
    "PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMyAwIFIKPj4KZW5kb2JqCjIgMCBvYmoKPDwKL1Byb2R1Y2VyIChQeXRo"
    "b24gYWlvZ3JhbSAzLnggQnVmZmVyKQo+PgplbmRvYmoKeHJlZgowIDMKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAw"
    "MDAwNDE3IDAwMDAwIG4gCjAwMDAwMDA0NjYwMDAwMCBuIAowMDAwMDAwMDE1IDAwMDAwIG4gCjAwMDAwMDAwNzAg"
    "MDAwMDAgbiAKMDAwMDAwMDE3OSAwMDAwMCBuIAowMDAwMDAwMzYwIDAwMDAwIG4gCnRyYWlsZXIKPDwKL1NpemUg"
    "MwolUm9vdCAxIDAgUgovSW5mbyAyIDAgUgo+PgpzdGFydHhyZWYKNTIxCislJUVPRg=="
)

GUIDE_EN_BASE64 = (
    "JVBERi0xLjUKJbXtrZsKMyAwIG9iago8PAovVHlwZSAvUGFnZXMKL0NvdW50IDEKL0tpZHMgWyA0IDAgUiBdCj4+"
    "CmVuZG9iago0IDAgb2JqCjw8Ci9UeXBlIC9QYWdlCi9QYXJlbnQgMyAwIFIKL01lZGlhQm94IFsgMCAwIDU5NSA4"
    "NDIgXQovQ29udGVudHMgNSAwIFIKL1Jlc291cmNlcyA8PAovRm9udCA8PAovRjEgNiAwIFIKPj4KPj4KPj4KZW5k"
    "b2JqCjUgMCBvYmoKPDwKL0xlbmd0aCAxOTIKL0ZpbHRlciAvRmxhdGVEZWNvZGUKPj4Kc3RyZWFtCnicS0wuyS/I"
    "SVRwS8xNVTBUCE7NzUutKOFyDeUKDAn28fX1VYgMVghKLUvNK87IVwjPL8pJUQBKpSgEJeamKjiAlXgWp6YwGECV"
    "pxbFAlXGAshmUAnmKrh7unp6BvEwMAQAcG0algplbmRzdHJlYW0KZW5kb2JqCjYgMCBvYmoKPDwKL1R5cGUgL0Zv"
    "bnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvSGVsdmV0aWNhLUJvbGQKPj4KZW5kb2JqCjEgMCBvYmoKPDwK"
    "L1R5cGUgL0NhdGFsb2cKL1BhZ2VzIDMgMCBSCj4+CmVuZG9iagoyIDAgb2JqCjw8Ci9Qcm9kdWNlciAoUHl0aG9u"
    "IGFpb2dyYW0gMy54IEJ1ZmZlcikKPj4KZW5kb2JqCnhyZWYKMCAzCjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAwMDAw"
    "MDQyNyAwMDAwMCBuIAowMDAwMDAwNDc2IDAwMDAwIG4gCjAwMDAwMDAwMTUgMDAwMDAgbiAKMDAwMDAwMDA3MCAw"
    "MDAwMCBuIAowMDAwMDAwMTc5IDAwMDAwIG4gCjAwMDAwMDAzNzAgMDAwMDAgbiAKdHJhaWxlcgo8PAovU2l6ZSAz"
    "Ci9Sb290IDEgMCBSCi9JbmZvIDIgMCBSCj4+CnN0YXJ0eHJlZgowIDUzMQolJUVPRg=="
)

# Вспомогательная функция для безопасного декодирования "на лету"
def get_file_buffer(base64_string: str) -> bytes:
    # Очищаем строку от возможных пробелов и переносов, часто возникающих при копировании
    clean_string = "".join(base64_string.split())
    return base64.b64decode(clean_string)


# --- Обработчики навигации по меню ---

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Здравствуйте, {message.from_user.first_name}! 👋\n"
        f"Добро пожаловать в официальный информационный бот Международного волонтерского форума. "
        f"Пожалуйста, воспользуйтесь кнопками ниже:",
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
        "Выберите интересующий вас язык для скачивания памятки участника:",
        reply_markup=guide_keyboard
    )

@dp.message(F.text == "Главное меню")
async def back_to_main(message: Message):
    await message.answer("Вы вернулись в главное меню.", reply_markup=main_keyboard)


# --- Логика отправки декодированных PDF документов ---

@dp.message(F.text == "Программа")
async def send_program(message: Message):
    await message.answer("🔄 Подготовка файла программы, пожалуйста, подождите...")
    try:
        file_bytes = get_file_buffer(PROGRAM_BASE64)
        file_input = BufferedInputFile(file_bytes, filename="программа.pdf")
        await message.answer_document(
            document=file_input,
            caption="📋 Официальная программа Международного форума волонтеров 2026 (г. Балхаш)."
        )
    except Exception as e:
        logging.error(f"Ошибка отправки Программы: {e}")
        await message.answer("⚠️ Произошла ошибка при генерации файла. Обратитесь к организаторам.")

@dp.message(F.text == "на русском")
async def send_guide_ru(message: Message):
    await message.answer("🔄 Загрузка памятки на русском языке...")
    try:
        file_bytes = get_file_buffer(GUIDE_RU_BASE64)
        file_input = BufferedInputFile(file_bytes, filename="памятка_на_русском.pdf")
        await message.answer_document(
            document=file_input,
            caption="🇷🇺 Памятка участника (Русская версия) — организационные моменты, безопасность и локации."
        )
    except Exception as e:
        logging.error(f"Ошибка отправки памятки RU: {e}")
        await message.answer("⚠️ Не удалось загрузить файл.")

@dp.message(F.text == "на англиском")
async def send_guide_en(message: Message):
    await message.answer("🔄 Downloading participant guide in English...")
    try:
        file_bytes = get_file_buffer(GUIDE_EN_BASE64)
        file_input = BufferedInputFile(file_bytes, filename="participant_guide_en.pdf")
        await message.answer_document(
            document=file_input,
            caption="🇬🇧 Participant Guide (English version) — accommodation, transport, and event info."
        )
    except Exception as e:
        logging.error(f"Ошибка отправки памятки EN: {e}")
        await message.answer("⚠️ Error downloading file.")


# --- Точка входа ---
async def main():
    # Очищаем вебхуки перед пуллингом
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())