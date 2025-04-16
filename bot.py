from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters, ConversationHandler
)

# Replace with your bot token and target group chat ID
BOT_TOKEN = '7576794460:AAHQPFMMU-nxzzy_GEjb4H8_v2vbFUSaE7s'
GROUP_CHAT_ID = -1002590049046  # Replace with your group ID

# States
CHOOSE_PLAN, AWAIT_RECEIPT = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Plan 1", callback_data='plan_1')],
        [InlineKeyboardButton("Plan 2", callback_data='plan_2')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Please choose your plan:", reply_markup=reply_markup)
    return CHOOSE_PLAN

async def handle_plan_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    plan = query.data
    context.user_data['plan'] = plan

    if plan == 'plan_1':
        await query.edit_message_text("You chose Plan 1. Great choice!")
    else:
        await query.edit_message_text("You chose Plan 2. Awesome!")

    await query.message.reply_text("Please upload your receipt (as image or document):")
    return AWAIT_RECEIPT

async def handle_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    plan = context.user_data.get('plan', 'Unknown')
    caption = f"📥 New Receipt Received\nFrom: @{user.username or user.full_name}\nPlan: {plan}"

    if update.message.photo:
        # It's a photo (use send_photo)
        photo = update.message.photo[-1]  # highest resolution
        await context.bot.send_photo(
            chat_id=GROUP_CHAT_ID,
            photo=photo.file_id,
            caption=caption
        )

    elif update.message.document:
        # It's a document (use send_document)
        doc = update.message.document
        await context.bot.send_document(
            chat_id=GROUP_CHAT_ID,
            document=doc.file_id,
            caption=caption
        )

    else:
        await update.message.reply_text("⚠️ Please upload a valid image or file.")
        return AWAIT_RECEIPT

    await update.message.reply_text("✅ Receipt received! Please wait for a response.")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSE_PLAN: [CallbackQueryHandler(handle_plan_choice)],
            AWAIT_RECEIPT: [MessageHandler(filters.PHOTO | filters.Document.ALL, handle_receipt)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == '__main__':
    main()
