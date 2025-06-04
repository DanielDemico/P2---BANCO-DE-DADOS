from typing import Optional

class ProdutoIngredientesModel:
    def __init__(self, fk_produto: int = 0, fk_ingrediente: int = 0, 
                 quantidade_necessaria: float = 0.0):
        self.fk_produto = fk_produto
        self.fk_ingrediente = fk_ingrediente
        self.quantidade_necessaria = quantidade_necessaria
    
    def __repr__(self):
        return f"ProdutoIngredientes(produto={self.fk_produto}, " \
               f"ingrediente={self.fk_ingrediente}, qtd={self.quantidade_necessaria})"
    
    def to_dict(self):
        return {
            'fk_produto': self.fk_produto,
            'fk_ingrediente': self.fk_ingrediente,
            'quantidade_necessaria': self.quantidade_necessaria
        } 