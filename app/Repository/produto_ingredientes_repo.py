import sqlite3
from typing import List, Optional, Dict
from Models.produto_ingredientes_model import ProdutoIngredientesModel
from db import get_connection

class ProdutoIngredientesRepository:
    def __init__(self):
        self.create_table()
    
    def create_table(self):
        """Create the produto_ingredientes table if it doesn't exist"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS produto_ingredientes (
                    fk_produto INTEGER NOT NULL,
                    fk_ingrediente INTEGER NOT NULL,
                    quantidade_necessaria REAL NOT NULL,
                    PRIMARY KEY (fk_produto, fk_ingrediente),
                    FOREIGN KEY (fk_produto) REFERENCES produtos(id_produto),
                    FOREIGN KEY (fk_ingrediente) REFERENCES ingredientes(id_ingrediente)
                )
            """)
    
    def add_ingrediente_ao_produto(self, composicao: ProdutoIngredientesModel) -> bool:
        with get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO produto_ingredientes (fk_produto, fk_ingrediente, quantidade_necessaria)
                    VALUES (?, ?, ?)
                """, (composicao.fk_produto, composicao.fk_ingrediente, 
                     composicao.quantidade_necessaria))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False
    
    def get_ingredientes_do_produto(self, fk_produto: int) -> List[Dict]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT i.id_ingrediente, i.nome_i, i.unidade, pi.quantidade_necessaria
                FROM produto_ingredientes pi
                JOIN ingredientes i ON pi.fk_ingrediente = i.id_ingrediente
                WHERE pi.fk_produto = ?
                ORDER BY i.nome_i
            """, (fk_produto,))
            return [{
                'id_ingrediente': row[0],
                'nome_ingrediente': row[1],
                'unidade': row[2],
                'quantidade_necessaria': row[3]
            } for row in cursor.fetchall()]
    
    def update_quantidade_ingrediente_produto(self, fk_produto: int, 
                                            fk_ingrediente: int, 
                                            nova_quantidade: float) -> bool:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE produto_ingredientes 
                SET quantidade_necessaria = ?
                WHERE fk_produto = ? AND fk_ingrediente = ?
            """, (nova_quantidade, fk_produto, fk_ingrediente))
            conn.commit()
            return cursor.rowcount > 0
    
    def remove_ingrediente_do_produto(self, fk_produto: int, fk_ingrediente: int) -> bool:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM produto_ingredientes 
                WHERE fk_produto = ? AND fk_ingrediente = ?
            """, (fk_produto, fk_ingrediente))
            conn.commit()
            return cursor.rowcount > 0
    
    def verificar_ingrediente_no_produto(self, fk_produto: int, fk_ingrediente: int) -> bool:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 1 FROM produto_ingredientes 
                WHERE fk_produto = ? AND fk_ingrediente = ?
            """, (fk_produto, fk_ingrediente))
            return cursor.fetchone() is not None 