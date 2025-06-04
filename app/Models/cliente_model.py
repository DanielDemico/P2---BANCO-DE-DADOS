from typing import Optional

class ClienteModel:
    def __init__(self, id_cliente: Optional[int] = None, nome: str = "", 
                 mesa: int = 1, cpf: str = ""):
        self.id_cliente = id_cliente
        self.nome = nome
        self.mesa = mesa
        self.cpf = cpf
    
    def __repr__(self):
        return f"Cliente(id={self.id_cliente}, nome={self.nome}, mesa={self.mesa}, cpf={self.cpf})"
    
    def to_dict(self):
        return {
            'id_cliente': self.id_cliente,
            'nome': self.nome,
            'mesa': self.mesa,
            'cpf': self.cpf
        }
    
    def get_all_clientes(self):
        return self.repository.get_all()
    
    def get_cliente_by_id(self, id):
        return self.repository.get_by_id(id)
    
    def create_cliente(self, nome, cpf, mesa, fk_pedido_venda):
        return self.repository.create(nome, cpf, mesa, fk_pedido_venda)
    
    def update_cliente(self, id, nome, cpf, mesa, fk_pedido_venda):
        return self.repository.update(id, nome, cpf, mesa, fk_pedido_venda)
    
    def delete_cliente(self, id):
        return self.repository.delete(id) 