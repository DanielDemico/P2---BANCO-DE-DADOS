from typing import Optional
from datetime import datetime

class PedidoVendaModel:
    def __init__(self, id_pedido_venda: Optional[int] = None, 
                 fk_cliente: int = 0, fk_produto: int = 0, 
                 qtd_venda: int = 0, data_venda: Optional[datetime] = None):
        self.id_pedido_venda = id_pedido_venda
        self.fk_cliente = fk_cliente
        self.fk_produto = fk_produto
        self.qtd_venda = qtd_venda
        self.data_venda = data_venda or datetime.now()
    
    def __repr__(self):
        return f"PedidoVenda(id={self.id_pedido_venda}, cliente={self.fk_cliente}, produto={self.fk_produto}, qtd={self.qtd_venda})"
    
    def to_dict(self):
        return {
            'id_pedido_venda': self.id_pedido_venda,
            'fk_cliente': self.fk_cliente,
            'fk_produto': self.fk_produto,
            'qtd_venda': self.qtd_venda,
            'data_venda': self.data_venda
        } 