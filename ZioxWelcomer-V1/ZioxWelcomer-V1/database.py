import sqlite3
conn=sqlite3.connect('data/bot.db')
conn.execute('CREATE TABLE IF NOT EXISTS settings(chat_id INTEGER PRIMARY KEY,rules TEXT DEFAULT "")')
conn.commit()
