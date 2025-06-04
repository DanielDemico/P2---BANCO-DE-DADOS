from Repository.fornecedor import FornecedorRepository
from typing import Optional

class FornecedorModel:
    def __init__(self, id_fornecedor: Optional[int] = None, nome: str = "", cnpj: str = ""):
        self.id_fornecedor = id_fornecedor
        self.nome = nome
        self.cnpj = cnpj
        self.repository = FornecedorRepository()
    
    def __repr__(self):
        return f"Fornecedor(id={self.id_fornecedor}, nome='{self.nome}', cnpj='{self.cnpj}')"
    
    def to_dict(self):
        return {
            'id_fornecedor': self.id_fornecedor,
            'nome': self.nome,
            'cnpj': self.cnpj
        }
    
    def get_all_fornecedores(self):
        return self.repository.get_all()
    
    def get_fornecedor_by_id(self, id):
        return self.repository.get_by_id(id)
    
    def create_fornecedor(self, cnpj, fk_pedido_compra, fk_ingredientes):
        return self.repository.create(cnpj, fk_pedido_compra, fk_ingredientes)
    
    def update_fornecedor(self, id, cnpj, fk_pedido_compra, fk_ingredientes):
        return self.repository.update(id, cnpj, fk_pedido_compra, fk_ingredientes)
    
    def delete_fornecedor(self, id):
        return self.repository.delete(id) 