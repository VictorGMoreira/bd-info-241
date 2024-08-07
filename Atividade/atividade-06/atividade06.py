  # models.py
  from pydantic import BaseModel

  class Aluno(BaseModel):
      aluno_nome: str
      endereco: str

  # database.py
  import sqlite3
  from typing import List

  class Database:
      def __init__(self, db_name: str):
          self.conn = sqlite3.connect(db_name)
          self.cursor = self.conn.cursor()

      def execute(self, query: str, params: tuple = None):
          if params:
              self.cursor.execute(query, params)
          else:
              self.cursor.execute(query)
          self.conn.commit()

      def fetchall(self):
          return self.cursor.fetchall()

      def close(self):
          self.conn.close()

  # routes.py
  from fastapi import FastAPI, HTTPException
  from typing import List
  from models import Aluno
  from database import Database

  app = FastAPI()

  db = Database('dbalunos.db')

  @app.post("/criar_aluno/", response_model=Aluno)
  async def criar_aluno(aluno: Aluno):
      db.execute("INSERT INTO TB_ALUNO (aluno_nome, endereco) VALUES (?, ?)", (aluno.aluno_nome, aluno.endereco))
      return aluno

  @app.get("/listar_alunos/", response_model=List[Aluno])
  async def listar_alunos():
      db.execute("SELECT * FROM TB_ALUNO")
      return [Aluno(**row) for row in db.fetchall()]

  # ...