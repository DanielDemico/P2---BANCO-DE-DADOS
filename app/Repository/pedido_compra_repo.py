import sqlite3
from typing import List, Optional, Dict
from Models.pedido_compra_model import PedidoCompraModel
from datetime import datetime
from db import get_connection

class PedidoCompraRepository:
    def __init__(self):
        self.create_table()
    
    def create_table(self):
        """Create the pedido_compra table if it doesn't exist"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pedido_compra (
                    id_pedido_compra INTEGER PRIMARY KEY AUTOINCREMENT,
                    fk_funcionario INTEGER NOT NULL,
                    fk_ingrediente INTEGER NOT NULL,
                    qtd_ingrediente REAL NOT NULL,
                    data_compra DATETIME NOT NULL,
                    FOREIGN KEY (fk_funcionario) REFERENCES funcionarios(id_funcionario),
                    FOREIGN KEY (fk_ingrediente) REFERENCES ingredientes(id_ingrediente)
                )
            """)
    
    def add_pedido_compra(self, pedido: PedidoCompraModel) -> PedidoCompraModel:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pedido_compra (fk_funcionario, fk_ingrediente, qtd_ingrediente, data_compra)
                VALUES (?, ?, ?, ?)
            """, (pedido.fk_funcionario, pedido.fk_ingrediente, 
                 pedido.qtd_ingrediente, pedido.data_compra))
            conn.commit()
            pedido.id_pedido_compra = cursor.lastrowid
            return pedido
    
    def get_all_pedidos_compra(self) -> List[PedidoCompraModel]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_pedido_compra, fk_funcionario, fk_ingrediente, qtd_ingrediente, data_compra 
                FROM pedido_compra
                ORDER BY data_compra DESC
            """)
            return [PedidoCompraModel(id_pedido_compra=row[0], fk_funcionario=row[1], 
                                    fk_ingrediente=row[2], qtd_ingrediente=row[3], 
                                    data_compra=datetime.fromisoformat(row[4]))
                   for row in cursor.fetchall()]
    
    def get_pedido_compra_by_id(self, id_pedido_compra: int) -> Optional[PedidoCompraModel]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_pedido_compra, fk_funcionario, fk_ingrediente, qtd_ingrediente, data_compra 
                FROM pedido_compra 
                WHERE id_pedido_compra = ?
            """, (id_pedido_compra,))
            row = cursor.fetchone()
            if row:
                return PedidoCompraModel(id_pedido_compra=row[0], fk_funcionario=row[1], 
                                       fk_ingrediente=row[2], qtd_ingrediente=row[3], 
                                       data_compra=datetime.fromisoformat(row[4]))
            return None
    
    def update_pedido_compra_status(self, id_pedido_compra: int, status: str):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE pedido_compra 
                SET status = ? 
                WHERE id_pedido_compra = ?
            """, (status, id_pedido_compra))
            conn.commit()
    
    def delete_pedido_compra(self, id_pedido_compra: int):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pedido_compra WHERE id_pedido_compra = ?", (id_pedido_compra,))
            conn.commit()
    
    def get_all_pedidos_compra_detalhado(self) -> List[Dict]:
        """Return list of pedidos with funcionario and ingrediente names"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT pc.id_pedido_compra, 
                       f.nome as nome_funcionario,
                       i.nome_i as nome_ingrediente,
                       pc.qtd_ingrediente,
                       pc.data_compra,
                       i.valor_compra * pc.qtd_ingrediente as valor_total
                FROM pedido_compra pc
                JOIN funcionarios f ON pc.fk_funcionario = f.id_funcionario
                JOIN ingredientes i ON pc.fk_ingrediente = i.id_ingrediente
                ORDER BY pc.data_compra DESC
            """)
            return [{
                'id_pedido_compra': row[0],
                'nome_funcionario': row[1],
                'nome_ingrediente': row[2],
                'qtd_ingrediente': row[3],
                'data_compra': datetime.fromisoformat(row[4]),
                'valor_total': row[5]
            } for row in cursor.fetchall()]