import sqlite3
from typing import List, Optional
from Models.fornecedor_model import FornecedorModel
from db import get_connection

class FornecedorRepository:
    def __init__(self):
        self.create_table()
    
    def create_table(self):
        """Create the fornecedores table if it doesn't exist"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fornecedores (
                    id_fornecedor INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cnpj TEXT UNIQUE NOT NULL
                )
            """)
    
    def add_fornecedor(self, fornecedor: FornecedorModel) -> FornecedorModel:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO fornecedores (nome, cnpj)
                VALUES (?, ?)
            """, (fornecedor.nome, fornecedor.cnpj))
            fornecedor.id_fornecedor = cursor.lastrowid
            return fornecedor
    
    def get_all_fornecedores(self) -> List[FornecedorModel]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_fornecedor, nome, cnpj FROM fornecedores")
            return [FornecedorModel(id_fornecedor=row[0], nome=row[1], cnpj=row[2])
                   for row in cursor.fetchall()]
    
    def get_fornecedor_by_id(self, id_fornecedor: int) -> Optional[FornecedorModel]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_fornecedor, nome, cnpj FROM fornecedores WHERE id_fornecedor = ?", 
                         (id_fornecedor,))
            row = cursor.fetchone()
            if row:
                return FornecedorModel(id_fornecedor=row[0], nome=row[1], cnpj=row[2])
            return None
    
    def get_fornecedor_by_cnpj(self, cnpj: str) -> Optional[FornecedorModel]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_fornecedor, nome, cnpj FROM fornecedores WHERE cnpj = ?", (cnpj,))
            row = cursor.fetchone()
            if row:
                return FornecedorModel(id_fornecedor=row[0], nome=row[1], cnpj=row[2])
            return None
    
    def update_fornecedor(self, id_fornecedor: int, fornecedor_data: FornecedorModel):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE fornecedores
                SET nome = ?
                WHERE id_fornecedor = ?
            """, (fornecedor_data.nome, id_fornecedor))
    
    def delete_fornecedor(self, id_fornecedor: int):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM fornecedores WHERE id_fornecedor = ?", (id_fornecedor,))
            conn.commit()
    
    def search_fornecedores_by_nome(self, nome: str) -> List[FornecedorModel]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_fornecedor, nome, cnpj 
                FROM fornecedores 
                WHERE nome LIKE ?
            """, (f"%{nome}%",))
            return [FornecedorModel(id_fornecedor=row[0], nome=row[1], cnpj=row[2])
                   for row in cursor.fetchall()]
    
    def check_dependencies(self, id_fornecedor: int) -> bool:
        """Check if fornecedor has any dependencies in ingredientes table"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) 
                FROM ingredientes 
                WHERE fk_fornecedor = ?
            """, (id_fornecedor,))
            count = cursor.fetchone()[0]
            return count > 0 