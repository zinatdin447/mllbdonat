from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler, ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

# Admin username
ADMIN_USERNAME = "@z1natdin"

# States for ConversationHandler
LANGUAGE, SELECT_AMOUNT, CONFIRM_ORDER, SEND_PROOF = range(4)

# Updated diamond prices
DIAMOND_PRICES = {
    "English": {
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
}

LANGUAGES = ["English", "Uzbek", "Russian"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(lang, callback_data=lang)] for lang in LANGUAGES]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please choose your language:", reply_markup=reply_markup)
    return LANGUAGE

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    selected_language = query.data
    context.user_data['language'] = selected_language

    diamond_data = DIAMOND_PRICES.get(selected_language, DIAMOND_PRICES["English"])
    keyboard = [[InlineKeyboardButton(f"{amt} - {price}", callback_data=amt)] for amt, price in diamond_data.items()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Select diamond amount:", reply_markup=reply_markup)
    return SELECT_AMOUNT

async def select_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    selected_amount = query.data
    context.user_data['amount'] = selected_amount
    lang = context.user_data.get('language', 'English')
    price = DIAMOND_PRICES[lang].get(selected_amount, "Unknown")

    await query.edit_message_text(f"You selected: {selected_amount}\nPrice: {price}\nPlease send payment proof.")
    return SEND_PROOF

async def handle_proof(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Thank you! We will verify your payment soon.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please type /start to begin your top-up.")

async def send_admin_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Contact admin: {ADMIN_USERNAME}")

async def send_prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('language', 'English')
    prices = "\n".join([f"{amount}: {price}" for amount, price in DIAMOND_PRICES[lang].items()])
    await update.message.reply_text(f"💎 Diamond Prices:\n{prices}")


def main():
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE: [CallbackQueryHandler(set_language)],
            SELECT_AMOUNT: [CallbackQueryHandler(select_amount)],
            SEND_PROOF: [MessageHandler(filters.TEXT | filters.PHOTO, handle_proof)]
        },
        fallbacks=[],
        allow_reentry=True
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("admin", send_admin_contact))
    application.add_handler(CommandHandler("prices", send_prices))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


if __name__ == '__main__':
    main()
