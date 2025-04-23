from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    CallbackQueryHandler, MessageHandler, ConversationHandler, filters
)
from telegram import BotCommand
from telegram.ext import Updater, CommandHandler
from telegram.ext import Updater, CommandHandler
import threading
import http.server
import socketserver


async def set_commands(application):
    await application.bot.set_my_commands([
        BotCommand("start", "Սկսել բոթը")
    ])

# Replace with your bot token and target group chat ID
BOT_TOKEN = '7576794460:AAHQPFMMU-nxzzy_GEjb4H8_v2vbFUSaE7s'
GROUP_CHAT_ID = -1002590049046  # Replace with your group ID

# Define states
CHOOSE_PLAN, AWAIT_RECEIPT = range(2)

print("🚀 bot.py is starting...")

# try:
#     from telegram.ext import Updater, CommandHandler
#     import threading
#     import http.server
#     import socketserver
#     print("✅ All modules imported.")
# except Exception as e:
#     print("❌ Import failed:", e)
#     raise

# def start(update, context):
#     update.message.reply_text("Hello from Cloud Run!")

# def run_bot():
#     print("🔁 Starting Telegram polling...")
#     updater = Updater("7576794460:AAHQPFMMU-nxzzy_GEjb4H8_v2vbFUSaE7s", use_context=True)  # Replace with actual token
#     dp = updater.dispatcher
#     dp.add_handler(CommandHandler("start", start))
#     updater.start_polling()
#     updater.idle()

# def run_http_server():
#     print("🌐 Starting HTTP server on port 8080...")
#     PORT = 8080
#     handler = http.server.SimpleHTTPRequestHandler
#     with socketserver.TCPServer(("", PORT), handler) as httpd:
#         httpd.serve_forever()

# threading.Thread(target=run_bot).start()
# run_http_server()

# Step 1: Start the bot with "Let's Go" button
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("«ԱՌԱՋ»", callback_data='lets_go')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Ուրախ եմ Ձեզ տեսնել Սկեսուրների բոտում 🥰🫶🏻\n\n"
    "«ԱՆՏԱՆԵԼԻ ՍԿԵՍՈՒՐ կամ պարզապես ՄԱՄԱՅԻ ՏՂԵՆ» դասընթացի մանրամասներին ծանոթանալու համար սեղմեք", reply_markup=reply_markup)
    return CHOOSE_PLAN

# Step 2: After "Let's Go" - show plan options
async def choose_plan_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("🎀 #1", callback_data='plan_1')],
        [InlineKeyboardButton("🎀 #2", callback_data='plan_2')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Ձեզ եմ առաջարկում դասընթացին միանալու երկու տարբերակ 🩶\n\n"
    "🎀 #1. Առաջինը՝\n\n"
    "«ԱՆՏԱՆԵԼԻ ՍԿԵՍՈՒՐ կամ պարզապես ՄԱՄԱՅԻ ՏՂԵՆ» դասընթացն է ԱՌԱՆՑ մեկնաբանության և այլ մասնակիցների հետ քննարկման հնարավորության:\n\n"
    "Արժեքը՝ 5️⃣0️⃣0️⃣0️⃣ՀՀ դրամ։\n\n"
    "🎀 #2. Երկրորդը՝\n\n"
    "«ԱՆՏԱՆԵԼԻ ՍԿԵՍՈՒՐ կամ պարզապես ՄԱՄԱՅԻ ՏՂԵՆ» դասընթացն է ԲԱՑ մեկնաբանություններով և այլ մասնակիցների հետ քննարկելու հնարավորությամբ։\n\n"
    "Արժեքը՝ 7️⃣5️⃣0️⃣0️⃣ՀՀ դրամ։\n\n"
    "Ո՞ր տարբերակին եք ցանկանում միանալ 🥰🫶🏻\n\n"
    "Սեղմեք համապատասխան կոճակին 🩶",
        reply_markup=reply_markup
    )
    return AWAIT_RECEIPT

# Step 3: Handle Plan Selection
async def handle_plan_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    plan = query.data
    context.user_data['plan'] = plan

    if plan == 'plan_1':
        await query.edit_message_text( "Շատ բարի։ 🩶🥰🫶🏻\n\n"
    "Դասընթացի Ձեր ընտրած տարբերակի արժեքն է 5️⃣0️⃣0️⃣0️⃣ՀՀ դրամ։\n\n"
    "Ահա՛ բանկային քարտի տվյալները 💳\n\n"
    "INECOBANK ✨\n\n"
    "ANI KARAGYOZOVA\n\n"
    "Հաշվեհամար:\n"
    "2050432282587001\n\n"
    "Քարտի համար:\n"
    "4578910000448765\n\n"
    "Փոխանցումն իրականացնելուն պես խնդրում եմ նկարել և ուղարկել ԿՏՐՈՆԸ։")
    elif plan == 'plan_2':
        await query.edit_message_text( "Շատ բարի։ 🩶🥰🫶🏻\n\n"
    "Դասընթացի Ձեր ընտրած տարբերակի արժեքն է 7️⃣5️⃣0️⃣0️⃣ՀՀ դրամ։\n\n"
    "Ահա՛ բանկային քարտի տվյալները 💳\n\n"
    "INECOBANK ✨\n\n"
    "ANI KARAGYOZOVA\n\n"
    "Հաշվեհամար:\n"
    "2050432282587001\n\n"
    "Քարտի համար:\n"
    "4578910000448765\n\n"
    "Փոխանցումն իրականացնելուն պես խնդրում եմ նկարել և ուղարկել ԿՏՐՈՆԸ։")

    return AWAIT_RECEIPT

# Step 4: Handle image or file upload
async def handle_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    plan = context.user_data.get('plan', 'Unknown')
    caption = f"📥 New Receipt\nFrom: @{user.username or user.full_name}\nPlan: {plan}"

    if update.message.photo:
        photo = update.message.photo[-1]
        await context.bot.send_photo(
            chat_id=GROUP_CHAT_ID,
            photo=photo.file_id,
            caption=caption
        )
    else:
        await context.bot.send_document(
            chat_id=GROUP_CHAT_ID,
            document=update.message.document.file_id,
            caption=caption
        )

    context.bot_data[update.effective_user.username] = update.effective_user.id

    # ✅ Store the user's chosen plan
    if "plans" not in context.bot_data:
        context.bot_data["plans"] = {}
    context.bot_data["plans"][update.effective_user.username] = plan

    await update.message.reply_text("Շնորհակալ եմ վստահության համար։ 🩶🥰🫶🏻"
    "Շուտով կհաստատեմ Ձեր միացումը «ԱՆՏԱՆԵԼԻ ՍԿԵՍՈՒՐ կամ պարզապես ՄԱՄԱՅԻ ՏՂԵՆ» դասընթացին 🩶🎀 "
    "(Հաստատումը կարող է տևել մինչև 1 օր)։")
    return ConversationHandler.END

# Optional: Cancel handler
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Operation cancelled.")
    return ConversationHandler.END

# ✅ Confirm command with different link for each plan
async def confirm_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Օգտագործեք՝ /confirm @username")
        return

    username = context.args[0].lstrip('@')
    user_id = context.bot_data.get(username)

    if not user_id:
        await update.message.reply_text("⚠️ Չի գտնվել ID այս username-ի համար։ Նա դեռ չի ուղարկել կտրոն։")
        return

    plan = context.bot_data.get("plans", {}).get(username)

    if plan == "plan_1":
        plan_link = "https://t.me/+PW675btAg3s0NDgy"  # Link for Plan 1
    elif plan == "plan_2":
        plan_link = "https://t.me/+GmAf3khB6bpkOGJi"  # Link for Plan 2
    else:
        plan_link = "https://t.me/fallback"  # Optional fallback

    try:
        await context.bot.send_message(
            chat_id=user_id,
            text="Ձեր միացումը հաստատված է։ 🩶🎀🎉\n\n"
                 "Արդեն ավելացրել եմ Ձեզ դասընթացի խմբին։🩶⬇️",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("«ԽՈՒՄԲ»", url=plan_link)]])
        )
        await update.message.reply_text(f"✅ Հաստատման նամակը ուղարկվեց @{username} օգտատիրոջը։")

    except Exception as e:
        await update.message.reply_text(f"❌ Չհաջողվեց ուղարկել նամակ @{username} օգտատիրոջը։\n{e}")

# Main function
def main():
    async def on_start(app):
        await set_commands(app)

    app = ApplicationBuilder().token(BOT_TOKEN).post_init(on_start).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSE_PLAN: [CallbackQueryHandler(choose_plan_prompt, pattern='lets_go')],
            AWAIT_RECEIPT: [
                CallbackQueryHandler(handle_plan_choice, pattern='^plan_'),
                MessageHandler(filters.PHOTO | filters.Document.ALL, handle_receipt)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    app.add_handler(CommandHandler('confirm', confirm_access))
    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == '__main__':
    main()
