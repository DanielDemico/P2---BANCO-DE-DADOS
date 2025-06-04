import sqlite3
from typing import List, Optional, Dict
from Models.pedido_venda_model import PedidoVendaModel
from datetime import datetime

class PedidoVendaRepository:
    def __init__(self):
        self.db_path = "villa.db"
    
    def _get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def add_pedido_venda(self, pedido: PedidoVendaModel) -> PedidoVendaModel:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pedido_venda (fk_cliente, fk_produto, qtd_venda, data_venda)
                VALUES (?, ?, ?, ?)
            """, (pedido.fk_cliente, pedido.fk_produto, 
                 pedido.qtd_venda, pedido.data_venda))
            pedido.id_pedido_venda = cursor.lastrowid
            return pedido
    
    def get_all_pedidos_venda(self) -> List[PedidoVendaModel]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_pedido_venda, fk_cliente, fk_produto, qtd_venda, data_venda 
                FROM pedido_venda
                ORDER BY data_venda DESC
            """)
            return [PedidoVendaModel(id_pedido_venda=row[0], fk_cliente=row[1], 
                                   fk_produto=row[2], qtd_venda=row[3], 
                                   data_venda=datetime.fromisoformat(row[4]))
                   for row in cursor.fetchall()]
    
    def get_pedido_venda_by_id(self, id_pedido_venda: int) -> Optional[PedidoVendaModel]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_pedido_venda, fk_cliente, fk_produto, qtd_venda, data_venda 
                FROM pedido_venda 
                WHERE id_pedido_venda = ?
            """, (id_pedido_venda,))
            row = cursor.fetchone()
            if row:
                return PedidoVendaModel(id_pedido_venda=row[0], fk_cliente=row[1], 
                                      fk_produto=row[2], qtd_venda=row[3], 
                                      data_venda=datetime.fromisoformat(row[4]))
            return None
    
    def delete_pedido_venda(self, id_pedido_venda: int):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pedido_venda WHERE id_pedido_venda = ?", 
                         (id_pedido_venda,))
    
    def get_all_pedidos_venda_detalhado(self) -> List[Dict]:
        """Return list of pedidos with cliente and produto names"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT pv.id_pedido_venda, 
                       c.nome as nome_cliente,
                       p.nome_p as nome_produto,
                       pv.qtd_venda,
                       pv.data_venda,
                       p.valor_venda * pv.qtd_venda as valor_total
                FROM pedido_venda pv
                JOIN clientes c ON pv.fk_cliente = c.id_cliente
                JOIN produtos p ON pv.fk_produto = p.id_produto
                ORDER BY pv.data_venda DESC
            """)
            return [{
                'id_pedido_venda': row[0],
                'nome_cliente': row[1],
                'nome_produto': row[2],
                'qtd_venda': row[3],
                'data_venda': datetime.fromisoformat(row[4]),
                'valor_total': row[5]
            } for row in cursor.fetchall()]
