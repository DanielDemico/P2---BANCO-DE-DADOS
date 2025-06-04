import sqlite3
from typing import List, Optional, Dict
from Models.ingrediente_model import IngredienteModel
from db import get_connection

class IngredienteRepository:
    def __init__(self):
        self.create_table()
    
    def create_table(self):
        """Create the ingredientes table if it doesn't exist"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ingredientes (
                    id_ingrediente INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_i TEXT NOT NULL,
                    valor_compra REAL NOT NULL,
                    quantidade REAL NOT NULL,
                    fk_fornecedor INTEGER NOT NULL,
                    FOREIGN KEY (fk_fornecedor) REFERENCES fornecedores(id_fornecedor)
                )
            """)
    
    def add_ingrediente(self, ingrediente: IngredienteModel) -> IngredienteModel:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO ingredientes (nome_i, valor_compra, quantidade, fk_fornecedor)
                VALUES (?, ?, ?, ?)
            """, (ingrediente.nome_i, ingrediente.valor_compra, 
                 ingrediente.quantidade, ingrediente.fk_fornecedor))
            ingrediente.id_ingrediente = cursor.lastrowid
            return ingrediente
    
    def get_all_ingredientes(self) -> List[IngredienteModel]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_ingrediente, nome_i, valor_compra, quantidade, fk_fornecedor 
                FROM ingredientes
            """)
            return [IngredienteModel(id_ingrediente=row[0], nome_i=row[1], 
                                   valor_compra=row[2], quantidade=row[3], 
                                   fk_fornecedor=row[4])
                   for row in cursor.fetchall()]
    
    def get_all_ingredientes_com_fornecedor(self) -> List[Dict]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT i.id_ingrediente, i.nome_i, i.valor_compra, i.quantidade, 
                       f.nome as nome_fornecedor
                FROM ingredientes i
                JOIN fornecedores f ON i.fk_fornecedor = f.id_fornecedor
                ORDER BY i.nome_i
            """)
            return [{
                'id_ingrediente': row[0],
                'nome_i': row[1],
                'valor_compra': row[2],
                'quantidade': row[3],
                'nome_fornecedor': row[4]
            } for row in cursor.fetchall()]
    
    def get_ingrediente_by_id(self, id_ingrediente: int) -> Optional[IngredienteModel]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_ingrediente, nome_i, valor_compra, quantidade, fk_fornecedor 
                FROM ingredientes 
                WHERE id_ingrediente = ?
            """, (id_ingrediente,))
            row = cursor.fetchone()
            if row:
                return IngredienteModel(id_ingrediente=row[0], nome_i=row[1], 
                                      valor_compra=row[2], quantidade=row[3], 
                                      fk_fornecedor=row[4])
            return None
    
    def update_ingrediente(self, id_ingrediente: int, ingrediente_data: IngredienteModel):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE ingredientes
                SET nome_i = ?, valor_compra = ?, quantidade = ?, fk_fornecedor = ?
                WHERE id_ingrediente = ?
            """, (ingrediente_data.nome_i, ingrediente_data.valor_compra, 
                 ingrediente_data.quantidade, ingrediente_data.fk_fornecedor, 
                 id_ingrediente))
    
    def delete_ingrediente(self, id_ingrediente: int):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ingredientes WHERE id_ingrediente = ?", (id_ingrediente,))
            conn.commit()
    
    def check_dependencies(self, id_ingrediente: int) -> bool:
        """Check if ingrediente has any dependencies in pedido_compra or produto_ingredientes tables"""
        with get_connection() as conn:
            cursor = conn.cursor()
            # Check pedido_compra
            cursor.execute("""
                SELECT COUNT(*) 
                FROM pedido_compra 
                WHERE fk_ingrediente = ?
            """, (id_ingrediente,))
            pedido_count = cursor.fetchone()[0]
            
            # Check produto_ingredientes
            cursor.execute("""
                SELECT COUNT(*) 
                FROM produto_ingredientes 
                WHERE fk_ingrediente = ?
            """, (id_ingrediente,))
            produto_count = cursor.fetchone()[0]
            
            return (pedido_count + produto_count) > 0 