import sqlite3
from datetime import datetime

class BancoDados:
    def __init__(self):
        self.con = sqlite3.connect("ranking.db")
        self.cur = self.con.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS ranking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jogador TEXT,
                pontuacao INTEGER,
                data_hora TEXT
            )
        """)
        self.con.commit()

    def salvar(self, jogador, pontos):
        data = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.cur.execute(
            "INSERT INTO ranking (jogador, pontuacao, data_hora) VALUES (?, ?, ?)",
            (jogador, pontos, data)
        )
        self.con.commit()

    def top5(self):
        self.cur.execute(
            "SELECT jogador, pontuacao, data_hora "
            "FROM ranking ORDER BY pontuacao DESC LIMIT 5"
        )
        return self.cur.fetchall()
