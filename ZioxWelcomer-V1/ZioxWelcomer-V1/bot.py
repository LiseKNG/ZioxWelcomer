from telegram import Update
from telegram.ext import Application,CommandHandler,MessageHandler,ContextTypes,filters
from config import TOKEN
import database
async def start(u,c): await u.message.reply_text('Bienvenue sur ZioxWelcomer')
async def rules(u,c): await u.message.reply_text('Aucune règle définie.')
async def welcome(u,c):
    for m in u.message.new_chat_members:
        await u.message.reply_text(f'👋 Bienvenue {m.full_name} !')
async def bye(u,c):
    await u.message.reply_text('Au revoir !')
app=Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler('start',start))
app.add_handler(CommandHandler('rules',rules))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS,welcome))
app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER,bye))
app.run_polling()
