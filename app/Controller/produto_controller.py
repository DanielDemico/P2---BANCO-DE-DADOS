from typing import List, Optional, Dict, Tuple
from Models.produto_model import ProdutoModel
from Repository.produto_repo import ProdutoRepository
from Repository.ingrediente_repo import IngredienteRepository

class ProdutoController:
    def __init__(self):
        self.repository = ProdutoRepository()
        self.ingrediente_repo = IngredienteRepository()
    
    def create_produto(self, nome: str, descricao: str, valor_venda: float, ingredientes: List[Tuple[int, float]]) -> Tuple[bool, str]:
        """Create a new produto with its ingredients and quantities"""
        try:
            if not nome:
                return False, "Nome do produto é obrigatório"
            
            if valor_venda <= 0:
                return False, "Valor de venda deve ser maior que zero"
            
            if not ingredientes:
                return False, "É necessário adicionar pelo menos um ingrediente"
            
            # Validate all ingredients exist
            for id_ingrediente, _ in ingredientes:
                if not self.ingrediente_repo.get_ingrediente_by_id(id_ingrediente):
                    return False, f"Ingrediente com ID {id_ingrediente} não encontrado"
            
            produto = ProdutoModel(nome_p=nome, descricao=descricao, valor_venda=valor_venda)
            self.repository.add_produto(produto, ingredientes)
            return True, "Produto criado com sucesso"
        except Exception as e:
            return False, f"Erro ao criar produto: {str(e)}"
    
    def list_produtos(self) -> List[ProdutoModel]:
        return self.repository.get_all_produtos()
    
    def get_produto(self, id_produto: int) -> Optional[ProdutoModel]:
        return self.repository.get_produto_by_id(id_produto)
    
    def get_produtos_para_display(self) -> List[Tuple[int, str, float]]:
        return self.repository.get_produtos_para_display()
    
    def update_produto_info(self, id_produto: int, nome: str, descricao: str, valor_venda: float) -> Tuple[bool, str]:
        try:
            # Validate input
            if not nome:
                return False, "Nome do produto é obrigatório"
            
            if valor_venda <= 0:
                return False, "Valor de venda deve ser maior que zero"
            
            # Check if produto exists
            produto = self.repository.get_produto_by_id(id_produto)
            if not produto:
                return False, "Produto não encontrado"
            
            # Update produto
            updated_produto = ProdutoModel(
                id_produto=id_produto,
                nome_p=nome,
                descricao=descricao,
                valor_venda=valor_venda
            )
            self.repository.update_produto(id_produto, updated_produto)
            return True, "Produto atualizado com sucesso"
        except Exception as e:
            return False, f"Erro ao atualizar produto: {str(e)}"
    
    def ajustar_estoque_produto(self, id_produto: int, 
                               quantidade_vendida_ou_comprada: int, 
                               operacao: str) -> Tuple[bool, str]:
        try:
            # Validate input
            if quantidade_vendida_ou_comprada <= 0:
                return False, "Quantidade deve ser maior que zero"
            
            if operacao not in ['venda', 'retorno']:
                return False, "Operação inválida. Use 'venda' ou 'retorno'"
            
            # Get current produto
            produto = self.repository.get_produto_by_id(id_produto)
            if not produto:
                return False, "Produto não encontrado"
            
            # Calculate new quantity
            nova_quantidade = produto.quantidade
            if operacao == 'venda':
                if produto.quantidade < quantidade_vendida_ou_comprada:
                    return False, "Estoque insuficiente"
                nova_quantidade -= quantidade_vendida_ou_comprada
            else:  # retorno
                nova_quantidade += quantidade_vendida_ou_comprada
            
            # Update stock
            self.repository.update_estoque(id_produto, nova_quantidade)
            return True, "Estoque atualizado com sucesso"
        except Exception as e:
            return False, f"Erro ao ajustar estoque: {str(e)}"
    
    def remove_produto(self, id_produto: int) -> Tuple[bool, str]:
        try:
            # Check if produto exists
            produto = self.repository.get_produto_by_id(id_produto)
            if not produto:
                return False, "Produto não encontrado"
            
            # Check only for pedido_venda dependencies
            if self.repository.check_pedido_venda_dependencies(id_produto):
                return False, "Não é possível remover este produto pois ele está sendo usado em pedidos de venda"
            
            # Remove produto
            self.repository.delete_produto(id_produto)
            return True, "Produto removido com sucesso"
        except Exception as e:
            return False, f"Erro ao remover produto: {str(e)}" 