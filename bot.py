from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler, ContextTypes

BOT_TOKEN = "7878111288:AAFKxb6ufAcH-rbR2c7ZMIS4Q43YR2bDD_c"
ADMIN_ID = 6358707501

# States
GET_LANGUAGE, GET_ID, GET_PACKAGE, GET_PROOF = range(4)

# Language dictionary
LANGUAGES = {
    "🇷🇺 Русский": "ru",
    "🇺🇿 O'zbek": "uz",
    "🇾🆫 Qaraqalpaq": "kkp"
}

# Available Packages
PACKAGES = {
    "50+50 Diamonds": "13 369 UZS",
    "150+150 Diamonds": "39 849 UZS",
    "250+250 Diamonds": "66 198 UZS",
    "500+500 Diamonds": "134 862 UZS",
    "11 Diamonds": "2 305 UZS",
    "22 Diamonds": "4 481 UZS", 
    "56 Diamonds": "11 286 UZS",
    "86 Diamonds": "17 740 UZS",
    "112 Diamonds": "22 665 UZS",
    "172 Diamonds": "35 172 UZS",
    "223 Diamonds": "45 330 UZS",
    "257 Diamonds": "50 906 UZS",
    "336 Diamonds": "67 867 UZS",
    "570 Diamonds": "113 198 UZS",
    "706 Diamonds": "138 217 UZS",
    "1163 Diamonds": "226 653 UZS"
}

# Messages in different languages with emojis
MESSAGES = {
    "start": {
        "ru": "💎 Добро пожаловать в ML Top-Up Bot! 🎮\n🚀 Здесь вы можете быстро и безопасно пополнить алмазы в Mobile Legends!\n💰 Выбирайте пакет и следуйте инструкциям!",
        "uz": "💎 ML Top-Up Bot-ga xush kelibsiz! 🎮\n🚀 Bu yerda siz Mobile Legends-ga tez va xavfsiz ravishda olmos sotib olishingiz mumkin!\n💰 Paketni tanlang va ko'rsatmalarga amal qiling!",
        "kkp": "💎 ML Top-Up Bot-ga xosh keldińiz! 🎮\n🚀 Mobile Legends ushın tez jáne qáwipsiz almaz satıp alıŋ!\n💰 Paketdi saylaŋ jáne instrukciyalardı orinlan!"
    },
    "enter_id": {
        "ru": "📏 Введите ID и сервер Mobile Legends (12345678(1234)):",
        "uz": "📏 Mobile Legends ID va serveringizni kiriting (masalan: 12345678(1234)):",
        "kkp": "📏 Mobile Legends ID jáne serverdí kiritiŋ (mısaly: 12345678(1234)):" 
    },
    "select_package": {
        "ru": "💎 Выберите пакет (цена указана):",
        "uz": "💎 Paketni tanlang (narxlari ko'rsatilgan):",
        "kkp": "💎 Paketdi saylaŋ (bađası kórsetílgen):"
    },
    "send_proof": {
        "ru": "📸 Пришлите скриншот или номер транзакции для подтверждения.",
        "uz": "📸 To'lov tasdig'i sifatida skrinshot yoki tranzaksiya raqamini yuboring.",
        "kkp": "📸 To'lemdi tastiyiq law ushın screenshot jiberiŋ"
    },
    "order_submitted": {
        "ru": "✅ Заказ отправлен! 🚀 Если в течение 4 часов заказ не выполнен, свяжитесь с админом.",
        "uz": "✅ Buyurtma yuborildi! 🚀 Agar 4 soat ichida bajarilmasa, administratorga murojaat qiling.",
        "kkp": "✅ Buyırtpanız jiberildi! 🚀 Eger 4 saat ishinдe bolmasa, adminge xabarlasıŋ."
    },
    "buy_again": {
        "ru": "🔁 Купить снова",
        "uz": "🔁 Qayta xarid qilish",
        "kkp": "🔁 Qaytadan satıp alıw"
    },
    "menu": {
        "ru": [["🔁 Купить снова", "📞 Админ"], ["📋 Прайс-лист"]],
        "uz": [["🔁 Qayta xarid", "📞 Admin"], ["📋 Narxlar ro'yxati"]],
        "kkp": [["🔁 Qaytadan alıw", "📞 Admin"], ["📋 Baha tizimi"]]
    }
}

user_data_store = {}

def get_custom_keyboard(lang_code):
    return ReplyKeyboardMarkup(MESSAGES["menu"][lang_code], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[InlineKeyboardButton(text=key, callback_data=value)] for key, value in LANGUAGES.items()]
    reply_markup = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(BIO_TEXT)
    await update.message.reply_text("🌍 Please select your language:", reply_markup=reply_markup)
    return GET_LANGUAGE

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    language = query.data

    user_data_store[query.from_user.id] = {"language": language}

    await query.message.reply_text(MESSAGES["enter_id"][language], reply_markup=get_custom_keyboard(language))
    return GET_ID

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = user_data_store[update.effective_user.id]
    user_data["ml_id"] = update.message.text

    buttons = [[InlineKeyboardButton(text=f"{key} ({PACKAGES[key]})", callback_data=key)] for key in PACKAGES.keys()]
    reply_markup = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(MESSAGES["select_package"][user_data["language"]], reply_markup=reply_markup)
    return GET_PACKAGE

async def get_package(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    package = query.data
    user_data = user_data_store[query.from_user.id]
    user_data["package"] = package

    await query.message.reply_text(MESSAGES["send_proof"][user_data["language"]])
    return GET_PROOF

async def get_proof(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = user_data_store.get(update.effective_user.id, {})

    if update.message.text:
        proof = update.message.text
    elif update.message.photo:
        photo = update.message.photo[-1]
        file = await photo.get_file()
        proof = f"Photo ID: {file.file_id}"
        await context.bot.send_photo(chat_id=ADMIN_ID, photo=file.file_id, caption=f"New order proof (photo)\nUser: @{update.effective_user.username}\nID: {update.effective_user.id}\nLang: {user_data.get('language')}\nML ID: {user_data.get('ml_id')}\nPackage: {user_data.get('package')}")
    else:
        proof = "Unknown format"

    if update.message.text:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"New order proof\nUser: @{update.effective_user.username}\nID: {update.effective_user.id}\nLang: {user_data.get('language')}\nML ID: {user_data.get('ml_id')}\nPackage: {user_data.get('package')}\nProof: {proof}"
        )

    buttons = [[InlineKeyboardButton(text=MESSAGES["buy_again"][user_data["language"]], callback_data="buy_again")]]
    reply_markup = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(MESSAGES["order_submitted"][user_data["language"]], reply_markup=reply_markup)
    return ConversationHandler.END

async def handle_buy_again(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    return await start(update, context)

async def handle_price_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data = user_data_store.get(user_id, {})
    lang = user_data.get("language", "uz")

    price_lines = [f"{name} – {price}" for name, price in PACKAGES.items()]
    header = {
        "ru": "Прайс-лист алмазов:",
        "uz": "Olmoslar narxlari:",
        "kkp": "Almaz baha tizimi:"
    }.get(lang, "Price List:")

    price_text = "💎 " + header + "\n\n" + "\n".join(price_lines)
    await update.message.reply_text(price_text)

def main():
    global BIO_TEXT
    BIO_TEXT = "📢 ML Top-Up Bot - ваш надежный помощник в пополнении алмазов Mobile Legends!\n👨‍💼 Админ: @z1natdin\n📢 Канал с подтверждениями: @mlbbdonatbotproof\nℹ️ Свяжитесь с нами, если у вас есть вопросы!"

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            GET_LANGUAGE: [CallbackQueryHandler(set_language)],
            GET_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_id)],
            GET_PACKAGE: [CallbackQueryHandler(get_package)],
            GET_PROOF: [MessageHandler(filters.ALL, get_proof)],
        },
        fallbacks=[]
    )
    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(handle_buy_again, pattern="^buy_again$"))
    app.add_handler(MessageHandler(filters.Regex("^(\ud83d\udccb Прайс-лист|\ud83d\udccb Narxlar ro'yxati|\ud83d\udccb Baha tizimi)$"), handle_price_list))
    app.run_polling()

if __name__ == '__main__':
    main()

