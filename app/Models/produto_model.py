from typing import Optional

class ProdutoModel:
    def __init__(self, id_produto: Optional[int] = None, nome_p: str = "", 
                 quantidade: int = 0, descricao: str = "", valor_venda: float = 0.0):
        self.id_produto = id_produto
        self.nome_p = nome_p
        self.quantidade = quantidade
        self.descricao = descricao
        self.valor_venda = valor_venda
    
    def __repr__(self):
        return f"Produto(id={self.id_produto}, nome='{self.nome_p}', estoque={self.quantidade}, valor={self.valor_venda})"
    
    def to_dict(self):
        return {
            'id_produto': self.id_produto,
            'nome_p': self.nome_p,
            'quantidade': self.quantidade,
            'descricao': self.descricao,
            'valor_venda': self.valor_venda
        } 