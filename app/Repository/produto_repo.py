import sqlite3
from typing import List, Optional, Dict, Tuple
from Models.produto_model import ProdutoModel
from db import get_connection

class ProdutoRepository:
    def __init__(self):
        self.create_table()
    
    def create_table(self):
        """Create the produtos table if it doesn't exist"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS produtos (
                    id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_p TEXT NOT NULL,
                    quantidade INTEGER NOT NULL,
                    descricao TEXT,
                    valor_venda REAL NOT NULL
                )
            """)
            
            # Create produto_ingredientes table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS produto_ingredientes (
                    id_produto_ingrediente INTEGER PRIMARY KEY AUTOINCREMENT,
                    fk_produto INTEGER NOT NULL,
                    fk_ingrediente INTEGER NOT NULL,
                    quantidade_necessaria REAL NOT NULL,
                    FOREIGN KEY (fk_produto) REFERENCES produtos(id_produto),
                    FOREIGN KEY (fk_ingrediente) REFERENCES ingredientes(id_ingrediente)
                )
            """)
    
    def add_produto(self, produto: ProdutoModel, ingredientes: List[Tuple[int, float]]) -> ProdutoModel:
        """Add a new produto with its ingredients and quantities"""
        with get_connection() as conn:
            cursor = conn.cursor()
            try:
                # Insert produto
                cursor.execute("""
                    INSERT INTO produtos (nome_p, quantidade, descricao, valor_venda)
                    VALUES (?, ?, ?, ?)
                """, (produto.nome_p, produto.quantidade, produto.descricao, produto.valor_venda))
                produto.id_produto = cursor.lastrowid
                
                # Insert ingredientes
                for id_ingrediente, quantidade in ingredientes:
                    cursor.execute("""
                        INSERT INTO produto_ingredientes (fk_produto, fk_ingrediente, quantidade_necessaria)
                        VALUES (?, ?, ?)
                    """, (produto.id_produto, id_ingrediente, quantidade))
                
                conn.commit()
                return produto
            except Exception as e:
                conn.rollback()
                raise e
    
    def get_all_produtos(self) -> List[ProdutoModel]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_produto, nome_p, quantidade, descricao, valor_venda 
                FROM produtos
                ORDER BY nome_p
            """)
            return [ProdutoModel(id_produto=row[0], nome_p=row[1], 
                               quantidade=row[2], descricao=row[3], 
                               valor_venda=row[4])
                   for row in cursor.fetchall()]
    
    def get_produto_by_id(self, id_produto: int) -> Optional[ProdutoModel]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_produto, nome_p, quantidade, descricao, valor_venda 
                FROM produtos 
                WHERE id_produto = ?
            """, (id_produto,))
            row = cursor.fetchone()
            if row:
                return ProdutoModel(id_produto=row[0], nome_p=row[1], 
                                  quantidade=row[2], descricao=row[3], 
                                  valor_venda=row[4])
            return None
    
    def update_produto(self, id_produto: int, produto_data: ProdutoModel):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE produtos
                SET nome_p = ?, quantidade = ?, descricao = ?, valor_venda = ?
                WHERE id_produto = ?
            """, (produto_data.nome_p, produto_data.quantidade,
                 produto_data.descricao, produto_data.valor_venda,
                 id_produto))
            conn.commit()
    
    def update_estoque(self, id_produto: int, nova_quantidade: int):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE produtos
                SET quantidade = ?
                WHERE id_produto = ?
            """, (nova_quantidade, id_produto))
            conn.commit()
    
    def delete_produto(self, id_produto: int):
        with get_connection() as conn:
            cursor = conn.cursor()
            try:
                # First delete related records in produto_ingredientes
                cursor.execute("DELETE FROM produto_ingredientes WHERE fk_produto = ?", (id_produto,))
                # Then delete the produto
                cursor.execute("DELETE FROM produtos WHERE id_produto = ?", (id_produto,))
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
    
    def check_pedido_venda_dependencies(self, id_produto: int) -> bool:
        """Check if produto has any dependencies in pedido_venda table"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) 
                FROM pedido_venda 
                WHERE fk_produto = ?
            """, (id_produto,))
            pedido_count = cursor.fetchone()[0]
            return pedido_count > 0
    
    def check_dependencies(self, id_produto: int) -> bool:
        """Check if produto has any dependencies in pedido_venda table"""
        return self.check_pedido_venda_dependencies(id_produto)
    
    def get_produtos_para_display(self) -> List[Tuple[int, str, float]]:
        """Return list of (id, nome, valor_venda) for selectboxes"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_produto, nome_p, valor_venda 
                FROM produtos 
                ORDER BY nome_p
            """)
            return [(row[0], row[1], row[2]) for row in cursor.fetchall()]
