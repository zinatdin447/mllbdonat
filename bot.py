from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler, ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

# States for ConversationHandler
SELECT_AMOUNT, CONFIRM_ORDER = range(2)

# Sample diamond prices
DIAMOND_PRICES = {
    "86 Diamonds": "$1.00",
    "172 Diamonds": "$2.00",
    "257 Diamonds": "$3.00",
    "344 Diamonds": "$4.00"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        KeyboardButton("Buy Again"),
        KeyboardButton("Admin")
    ], [
        KeyboardButton("Prices")
    ]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Welcome to the MLBB Top-up Bot! Choose an option:", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Buy Again":
        return await start_buy_flow(update, context)
    elif text == "Admin":
        return await send_admin_contact(update, context)
    elif text == "Prices":
        return await send_prices(update, context)
    else:
        await update.message.reply_text("Please choose an option from the keyboard.")

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


