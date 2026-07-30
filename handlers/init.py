"""
handlers/__init__.py

Enregistre tous les handlers du bot.
"""

# ======================================================
# IMPORTS
# ======================================================

from telegram.ext import Application

from .commands import register_commands
from .welcome import register_welcome
from .goodbye import register_goodbye
from .admin import register_admin


# ======================================================
# REGISTER
# ======================================================

def register_handlers(app: Application) -> None:
    """
    Enregistre tous les handlers.
    """

    register_commands(app)
    register_welcome(app)
    register_goodbye(app)
    register_admin(app)
