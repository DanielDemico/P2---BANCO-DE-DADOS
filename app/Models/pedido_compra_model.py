from typing import Optional
from datetime import datetime

class PedidoCompraModel:
    def __init__(self, id_pedido_compra: Optional[int] = None, 
                 fk_funcionario: int = 0, fk_ingrediente: int = 0, 
                 qtd_ingrediente: float = 0.0, data_compra: Optional[datetime] = None):
        self.id_pedido_compra = id_pedido_compra
        self.fk_funcionario = fk_funcionario
        self.fk_ingrediente = fk_ingrediente
        self.qtd_ingrediente = qtd_ingrediente
        self.data_compra = data_compra or datetime.now()
    
    def __repr__(self):
        return f"PedidoCompra(id={self.id_pedido_compra}, funcionario={self.fk_funcionario}, " \
               f"ingrediente={self.fk_ingrediente}, qtd={self.qtd_ingrediente})"
    
    def to_dict(self):
        return {
            'id_pedido_compra': self.id_pedido_compra,
            'fk_funcionario': self.fk_funcionario,
            'fk_ingrediente': self.fk_ingrediente,
            'qtd_ingrediente': self.qtd_ingrediente,
            'data_compra': self.data_compra
        } 