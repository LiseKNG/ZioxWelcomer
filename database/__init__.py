"""
database/__init__.py

Point d'entrée du package database.
"""

# ======================================================
# IMPORTS
# ======================================================

from .groups import (
    initialize_groups,
    create_group,
    get_group,
    set_welcome,
    set_goodbye,
    set_rules,
)

from .members import (
    initialize_members,
    add_member,
    remove_member,
)

from .logs import (
    initialize_logs,
    add_log,
)

from .settings import (
    initialize_settings,
    get_setting,
    set_setting,
)


# ======================================================
# INITIALISATION GLOBALE
# ======================================================

async def initialize_database():
    """
    Initialise toutes les tables de la base de données.
    """

    await initialize_groups()
    await initialize_members()
    await initialize_logs()
    await initialize_settings()
