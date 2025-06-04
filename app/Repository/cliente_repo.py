import sqlite3
from typing import List, Optional
from Models.cliente_model import ClienteModel
from db import get_connection

class ClienteRepository:
    def __init__(self):
        self.create_table()
    
    def create_table(self):
        """Create the clientes table if it doesn't exist"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    mesa INTEGER NOT NULL,
                    cpf TEXT UNIQUE NOT NULL
                )
            """)
    
    def add_cliente(self, cliente: ClienteModel) -> ClienteModel:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO clientes (nome, mesa, cpf)
                VALUES (?, ?, ?)
            """, (cliente.nome, cliente.mesa, cliente.cpf))
            cliente.id_cliente = cursor.lastrowid
            return cliente
    
    def get_all_clientes(self) -> List[ClienteModel]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_cliente, nome, mesa, cpf FROM clientes")
            return [ClienteModel(id_cliente=row[0], nome=row[1], mesa=row[2], cpf=row[3])
                   for row in cursor.fetchall()]
    
    def get_cliente_by_id(self, id_cliente: int) -> Optional[ClienteModel]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_cliente, nome, mesa, cpf FROM clientes WHERE id_cliente = ?", 
                         (id_cliente,))
            row = cursor.fetchone()
            if row:
                return ClienteModel(id_cliente=row[0], nome=row[1], mesa=row[2], cpf=row[3])
            return None
    
    def get_cliente_by_cpf(self, cpf: str) -> Optional[ClienteModel]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_cliente, nome, mesa, cpf FROM clientes WHERE cpf = ?", (cpf,))
            row = cursor.fetchone()
            if row:
                return ClienteModel(id_cliente=row[0], nome=row[1], mesa=row[2], cpf=row[3])
            return None
    
    def update_cliente(self, id_cliente: int, cliente_data: ClienteModel):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE clientes
                SET nome = ?, mesa = ?
                WHERE id_cliente = ?
            """, (cliente_data.nome, cliente_data.mesa, id_cliente))
    
    def delete_cliente(self, id_cliente: int):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clientes WHERE id_cliente = ?", (id_cliente,))
            conn.commit()
    
    def search_clientes_by_nome(self, nome: str) -> List[ClienteModel]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_cliente, nome, mesa, cpf 
                FROM clientes 
                WHERE nome LIKE ?
            """, (f"%{nome}%",))
            return [ClienteModel(id_cliente=row[0], nome=row[1], mesa=row[2], cpf=row[3])
                   for row in cursor.fetchall()]