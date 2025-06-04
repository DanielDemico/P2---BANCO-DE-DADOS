from Repository.ingredientes_repo import IngredienteRepository
from typing import Optional

class IngredienteModel:
    def __init__(self, id_ingrediente: Optional[int] = None, nome_i: str = "", 
                 valor_compra: float = 0.0, quantidade: float = 0.0, 
                 fk_fornecedor: int = 0):
        self.id_ingrediente = id_ingrediente
        self.nome_i = nome_i
        self.valor_compra = valor_compra
        self.quantidade = quantidade
        self.fk_fornecedor = fk_fornecedor
        self.repository = IngredienteRepository()
    
    def __repr__(self):
        return f"Ingrediente(id={self.id_ingrediente}, nome='{self.nome_i}', " \
               f"valor={self.valor_compra}, quantidade={self.quantidade})"
    
    def to_dict(self):
        return {
            'id_ingrediente': self.id_ingrediente,
            'nome_i': self.nome_i,
            'valor_compra': self.valor_compra,
            'quantidade': self.quantidade,
            'fk_fornecedor': self.fk_fornecedor
        }
    
    def get_all_ingredientes(self):
        return self.repository.get_all()
    
    def get_ingrediente_by_id(self, id):
        return self.repository.get_by_id(id)
    
    def create_ingrediente(self, quantidade, validade, desc, custo, fk_produto, fk_fornecedor):
        return self.repository.create(quantidade, validade, desc, custo, fk_produto, fk_fornecedor)
    
    def update_ingrediente(self, id, quantidade, validade, desc, custo, fk_produto, fk_fornecedor):
        return self.repository.update(id, quantidade, validade, desc, custo, fk_produto, fk_fornecedor)
    
    def delete_ingrediente(self, id):
        return self.repository.delete(id) 