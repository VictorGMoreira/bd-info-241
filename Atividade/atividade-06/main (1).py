import sqlite3
from typing import List, Optional, Tuple


class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def execute(self, query: str, params: Optional[Tuple] = None, commit: bool = True):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            if commit:
                self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def fetchall(self) -> List[Tuple]:
        return self.cursor.fetchall()

    def close(self):
        if self.conn:
            self.conn.close()

    def init_db(self):
        self.execute('''
            CREATE TABLE IF NOT EXISTS TB_ALUNO (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_nome TEXT NOT NULL,
                endereco TEXT NOT NULL
            )
        ''', commit=True)

    def __del__(self):
        self.close()

# Example usage
if __name__ == "__main__":
    db = Database('example.db')
    db.init_db()

    # Example of inserting data
    db.execute('INSERT INTO TB_ALUNO (aluno_nome, endereco) VALUES (?, ?)', ('John Doe', '123 Elm St'))

    # Example of querying data
    db.execute('SELECT * FROM TB_ALUNO')
    results = db.fetchall()
    for row in results:
        print(row)

    db.close()
