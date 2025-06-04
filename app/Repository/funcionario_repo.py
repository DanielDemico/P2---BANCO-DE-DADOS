import sqlite3
from typing import List, Optional
from Models.funcionario_model import FuncionarioModel
from db import get_connection
from datetime import date

class FuncionarioRepository:
    def __init__(self):
        self.create_table()
    
    def create_table(self):
        """Create the funcionarios table if it doesn't exist"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS funcionarios (
                    id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    dt_nascimento DATE NOT NULL,
                    cpf TEXT UNIQUE NOT NULL
                )
            """)
    
    def add_funcionario(self, funcionario: FuncionarioModel) -> FuncionarioModel:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO funcionarios (nome, dt_nascimento, cpf)
                VALUES (?, ?, ?)
            """, (funcionario.nome, funcionario.dt_nascimento, funcionario.cpf))
            funcionario.id_funcionario = cursor.lastrowid
            return funcionario
    
    def get_all_funcionarios(self) -> List[FuncionarioModel]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_funcionario, nome, dt_nascimento, cpf FROM funcionarios")
            return [FuncionarioModel(id_funcionario=row[0], nome=row[1], 
                                   dt_nascimento=date.fromisoformat(row[2]), cpf=row[3])
                   for row in cursor.fetchall()]
    
    def get_funcionario_by_id(self, id_funcionario: int) -> Optional[FuncionarioModel]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_funcionario, nome, dt_nascimento, cpf FROM funcionarios WHERE id_funcionario = ?", 
                         (id_funcionario,))
            row = cursor.fetchone()
            if row:
                return FuncionarioModel(id_funcionario=row[0], nome=row[1], 
                                      dt_nascimento=date.fromisoformat(row[2]), cpf=row[3])
            return None
    
    def get_funcionario_by_cpf(self, cpf: str) -> Optional[FuncionarioModel]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_funcionario, nome, dt_nascimento, cpf FROM funcionarios WHERE cpf = ?", (cpf,))
            row = cursor.fetchone()
            if row:
                return FuncionarioModel(id_funcionario=row[0], nome=row[1], 
                                      dt_nascimento=date.fromisoformat(row[2]), cpf=row[3])
            return None
    
    def update_funcionario(self, id_funcionario: int, funcionario_data: FuncionarioModel):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE funcionarios
                SET nome = ?, dt_nascimento = ?
                WHERE id_funcionario = ?
            """, (funcionario_data.nome, funcionario_data.dt_nascimento, id_funcionario))
    
    def delete_funcionario(self, id_funcionario: int):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM funcionarios WHERE id_funcionario = ?", (id_funcionario,))
            conn.commit()
    
    def verify_login(self, cpf: str, chave: str) -> Optional[FuncionarioModel]:
        funcionario = self.get_funcionario_by_cpf(cpf)
        if funcionario and funcionario.verify_chave(chave):
            return funcionario
        return None





