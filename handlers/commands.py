"""
handlers/commands.py

Gestion des commandes publiques.
"""

# ======================================================
# IMPORTS
# ======================================================

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from database import database


# ======================================================
# COMMANDES
# ======================================================

async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """
    Commande /start
    """

    if update.effective_chat:

        await database.create_group(
            update.effective_chat.id,
            update.effective_chat.title or "Conversation privée",
        )

    await update.message.reply_text(
        "👋 Bonjour !\n\n"
        "Je suis ZioxWelcomer.\n"
        "Utilise /help pour voir toutes mes commandes."
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """
    Commande /help
    """

    text = (
        "📚 Commandes disponibles\n\n"
        "/start - Démarrer le bot\n"
        "/help - Afficher cette aide\n"
        "/rules - Voir les règles du groupe"
    )

    await update.message.reply_text(text)


async def rules_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """
    Commande /rules
    """

    chat = update.effective_chat

    group = await database.get_group(chat.id)

    if not group:
        await update.message.reply_text(
            "Aucune règle n'a encore été configurée."
        )
        return

    rules = group["rules"]

    if not rules:
        rules = "Aucune règle n'a encore été configurée."

    await update.message.reply_text(rules)


# ======================================================
# ENREGISTREMENT
# ======================================================

def register_commands(app: Application):
    """
    Enregistre les commandes.
    """

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("rules", rules_command))
