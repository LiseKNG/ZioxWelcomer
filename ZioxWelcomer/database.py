"""
database.py

Gestion de la base de données SQLite de ZioxWelcomer.

Toutes les opérations SQL passent par cette classe.
"""

# ======================================================
# IMPORTS
# ======================================================

import aiosqlite

from config import DATABASE_PATH


# ======================================================
# DATABASE
# ======================================================

class Database:
    """
    Classe responsable de toutes les opérations SQL.
    """

    def __init__(self):
        """
        Initialise le chemin de la base de données.
        """
        self.db_path = DATABASE_PATH

    # ==================================================
    # INITIALISATION
    # ==================================================

    async def initialize(self):
        """
        Crée toutes les tables nécessaires au fonctionnement du bot.

        Cette méthode est appelée une seule fois au démarrage.
        """

        async with aiosqlite.connect(self.db_path) as db:

            # ==========================================
            # TABLE GROUPS
            # ==========================================

            await db.execute("""
            CREATE TABLE IF NOT EXISTS groups (

                chat_id INTEGER PRIMARY KEY,

                title TEXT,

                language TEXT DEFAULT 'fr',

                welcome_enabled INTEGER DEFAULT 1,
                goodbye_enabled INTEGER DEFAULT 1,
                captcha_enabled INTEGER DEFAULT 0,

                welcome_message TEXT DEFAULT '👋 Bienvenue {user} sur {group} !',

                goodbye_message TEXT DEFAULT '👋 {user} a quitté le groupe.',

                rules TEXT DEFAULT '',

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
            """)

            # ==========================================
            # TABLE MEMBERS
            # ==========================================

            await db.execute("""
            CREATE TABLE IF NOT EXISTS members (

                user_id INTEGER,

                chat_id INTEGER,

                username TEXT,

                first_name TEXT,

                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                PRIMARY KEY(user_id, chat_id)

            )
            """)

            # ==========================================
            # TABLE SETTINGS
            # ==========================================

            await db.execute("""
            CREATE TABLE IF NOT EXISTS settings (

                chat_id INTEGER,

                key TEXT,

                value TEXT,

                PRIMARY KEY(chat_id, key)

            )
            """)

            # ==========================================
            # TABLE LOGS
            # ==========================================

            await db.execute("""
            CREATE TABLE IF NOT EXISTS logs (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                chat_id INTEGER,

                user_id INTEGER,

                action TEXT,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
            """)

            await db.commit()

    # ==================================================
    # GROUPS
    # ==================================================

    async def create_group(self, chat_id: int, title: str):
        """
        Crée un groupe s'il n'existe pas.
        """

        async with aiosqlite.connect(self.db_path) as db:

            await db.execute(
                """
                INSERT OR IGNORE INTO groups(chat_id, title)
                VALUES (?, ?)
                """,
                (chat_id, title)
            )

            await db.commit()

    async def get_group(self, chat_id: int):
        """
        Retourne les informations d'un groupe.
        """

        async with aiosqlite.connect(self.db_path) as db:

            cursor = await db.execute(
                """
                SELECT *
                FROM groups
                WHERE chat_id = ?
                """,
                (chat_id,)
            )

            return await cursor.fetchone()

    async def set_welcome(self, chat_id: int, message: str):
        """
        Modifie le message de bienvenue.
        """

        async with aiosqlite.connect(self.db_path) as db:

            await db.execute(
                """
                UPDATE groups
                SET welcome_message = ?
                WHERE chat_id = ?
                """,
                (message, chat_id)
            )

            await db.commit()

    async def set_goodbye(self, chat_id: int, message: str):
        """
        Modifie le message d'au revoir.
        """

        async with aiosqlite.connect(self.db_path) as db:

            await db.execute(
                """
                UPDATE groups
                SET goodbye_message = ?
                WHERE chat_id = ?
                """,
                (message, chat_id)
            )

            await db.commit()

    async def set_rules(self, chat_id: int, rules: str):
        """
        Modifie les règles d'un groupe.
        """

        async with aiosqlite.connect(self.db_path) as db:

            await db.execute(
                """
                UPDATE groups
                SET rules = ?
                WHERE chat_id = ?
                """,
                (rules, chat_id)
            )

            await db.commit()

    # ==================================================
    # MEMBERS
    # ==================================================

    async def add_member(
        self,
        chat_id: int,
        user_id: int,
        username: str | None,
        first_name: str,
    ):
        """
        Ajoute ou met à jour un membre.
        """

        async with aiosqlite.connect(self.db_path) as db:

            await db.execute(
                """
                INSERT OR REPLACE INTO members
                (
                    user_id,
                    chat_id,
                    username,
                    first_name
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    user_id,
                    chat_id,
                    username,
                    first_name,
                )
            )

            await db.commit()

    async def remove_member(self, chat_id: int, user_id: int):
        """
        Supprime un membre de la base.
        """

        async with aiosqlite.connect(self.db_path) as db:

            await db.execute(
                """
                DELETE FROM members
                WHERE chat_id = ?
                AND user_id = ?
                """,
                (
                    chat_id,
                    user_id,
                )
            )

            await db.commit()

    # ==================================================
    # SETTINGS
    # ==================================================

    async def set_setting(
        self,
        chat_id: int,
        key: str,
        value: str,
    ):
        """
        Enregistre un paramètre du groupe.
        """

        async with aiosqlite.connect(self.db_path) as db:

            await db.execute(
                """
                INSERT OR REPLACE INTO settings
                (
                    chat_id,
                    key,
                    value
                )
                VALUES (?, ?, ?)
                """,
                (
                    chat_id,
                    key,
                    value,
                )
            )

            await db.commit()

    async def get_setting(
        self,
        chat_id: int,
        key: str,
    ):
        """
        Récupère un paramètre du groupe.
        """

        async with aiosqlite.connect(self.db_path) as db:

            cursor = await db.execute(
                """
                SELECT value
                FROM settings
                WHERE chat_id = ?
                AND key = ?
                """,
                (
                    chat_id,
                    key,
                )
            )

            result = await cursor.fetchone()

            return result[0] if result else None

    # ==================================================
    # LOGS
    # ==================================================

    async def log(
        self,
        chat_id: int,
        user_id: int,
        action: str,
    ):
        """
        Ajoute une entrée dans les logs.
        """

        async with aiosqlite.connect(self.db_path) as db:

            await db.execute(
                """
                INSERT INTO logs
                (
                    chat_id,
                    user_id,
                    action
                )
                VALUES (?, ?, ?)
                """,
                (
                    chat_id,
                    user_id,
                    action,
                )
            )

            await db.commit()


# ======================================================
# INSTANCE GLOBALE
# ======================================================

database = Database()
