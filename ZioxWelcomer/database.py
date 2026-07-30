import aiosqlite
from config import DATABASE_PATH


class Database:

    def __init__(self):
        self.db_path = DATABASE_PATH

    async def initialize(self):
        """Création des tables"""

        async with aiosqlite.connect(self.db_path) as db:

            # Configuration des groupes
            await db.execute("""
            CREATE TABLE IF NOT EXISTS groups(
                chat_id INTEGER PRIMARY KEY,
                title TEXT,
                language TEXT DEFAULT 'fr',

                welcome_enabled INTEGER DEFAULT 1,
                goodbye_enabled INTEGER DEFAULT 1,
                captcha_enabled INTEGER DEFAULT 0,

                welcome_message TEXT DEFAULT '👋 Bienvenue {user} !',
                goodbye_message TEXT DEFAULT '👋 {user} a quitté le groupe.',
                rules TEXT DEFAULT ''
            )
            """)

            # Membres
            await db.execute("""
            CREATE TABLE IF NOT EXISTS members(
                user_id INTEGER,
                chat_id INTEGER,

                username TEXT,
                first_name TEXT,

                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                PRIMARY KEY(user_id, chat_id)
            )
            """)

            # Journal des événements
            await db.execute("""
            CREATE TABLE IF NOT EXISTS logs(
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                chat_id INTEGER,
                user_id INTEGER,

                action TEXT,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            await db.commit()

    async def create_group(self, chat_id: int, title: str):

        async with aiosqlite.connect(self.db_path) as db:

            await db.execute("""
            INSERT OR IGNORE INTO groups(chat_id,title)
            VALUES(?,?)
            """, (chat_id, title))

            await db.commit()

    async def get_group(self, chat_id: int):

        async with aiosqlite.connect(self.db_path) as db:

            cursor = await db.execute("""
            SELECT *
            FROM groups
            WHERE chat_id=?
            """, (chat_id,))

            return await cursor.fetchone()

    async def set_welcome(self, chat_id: int, message: str):

        async with aiosqlite.connect(self.db_path) as db:

            await db.execute("""
            UPDATE groups
            SET welcome_message=?
            WHERE chat_id=?
            """, (message, chat_id))

            await db.commit()

    async def set_rules(self, chat_id: int, rules: str):

        async with aiosqlite.connect(self.db_path) as db:

            await db.execute("""
            UPDATE groups
            SET rules=?
            WHERE chat_id=?
            """, (rules, chat_id))

            await db.commit()

    async def add_member(
        self,
        chat_id: int,
        user_id: int,
        username: str,
        first_name: str
    ):

        async with aiosqlite.connect(self.db_path) as db:

            await db.execute("""
            INSERT OR REPLACE INTO members(
                user_id,
                chat_id,
                username,
                first_name
            )
            VALUES(?,?,?,?)
            """, (
                user_id,
                chat_id,
                username,
                first_name
            ))

            await db.commit()

    async def remove_member(self, chat_id: int, user_id: int):

        async with aiosqlite.connect(self.db_path) as db:

            await db.execute("""
            DELETE FROM members
            WHERE chat_id=?
            AND user_id=?
            """, (
                chat_id,
                user_id
            ))

            await db.commit()

    async def log(
        self,
        chat_id: int,
        user_id: int,
        action: str
    ):

        async with aiosqlite.connect(self.db_path) as db:

            await db.execute("""
            INSERT INTO logs(
                chat_id,
                user_id,
                action
            )
            VALUES(?,?,?)
            """, (
                chat_id,
                user_id,
                action
            ))

            await db.commit()


database = Database()
