from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler, ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

# States for ConversationHandler
SELECT_AMOUNT, CONFIRM_ORDER = range(2)

# Updated diamond prices
DIAMOND_PRICES = {
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the MLBB Top-up Bot! Type /start to begin your order.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please type /start to begin your top-up.")

async def send_admin_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Contact admin: @youradminusername")

async def send_prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prices = "\n".join([f"{amount}: {price}" for amount, price in DIAMOND_PRICES.items()])
    await update.message.reply_text(f"💎 Diamond Prices:\n{prices}")

async def start_buy_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(amount, callback_data=amount)] for amount in DIAMOND_PRICES.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please choose how many diamonds you want:", reply_markup=reply_markup)
    return SELECT_AMOUNT

async def select_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['amount'] = query.data
    await query.edit_message_text(f"You selected {query.data}. Please confirm your order.")
    return CONFIRM_ORDER

async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Thanks for your order. Please send payment proof.")
    return ConversationHandler.END

def main():
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECT_AMOUNT: [CallbackQueryHandler(select_amount)],
            CONFIRM_ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_order)]
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()




