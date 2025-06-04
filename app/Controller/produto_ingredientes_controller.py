from typing import List, Optional, Dict, Tuple
from Models.produto_ingredientes_model import ProdutoIngredientesModel
from Repository.produto_ingredientes_repo import ProdutoIngredientesRepository
from Controller.produto_controller import ProdutoController
from Controller.ingrediente_controller import IngredienteController

class ProdutoIngredientesController:
    def __init__(self):
        self.repository = ProdutoIngredientesRepository()
        self.produto_controller = ProdutoController()
        self.ingrediente_controller = IngredienteController()
    
    def add_composicao(self, fk_produto: int, fk_ingrediente: int, 
                      qtd: float) -> Tuple[bool, str]:
        try:
            # Validate input
            if qtd <= 0:
                return False, "Quantidade deve ser maior que zero"
            
            # Check if produto exists
            produto = self.produto_controller.get_produto(fk_produto)
            if not produto:
                return False, "Produto não encontrado"
            
            # Check if ingrediente exists
            ingrediente = self.ingrediente_controller.get_ingrediente_by_id(fk_ingrediente)
            if not ingrediente:
                return False, "Ingrediente não encontrado"
            
            # Check if ingrediente is already in produto
            if self.repository.verificar_ingrediente_no_produto(fk_produto, fk_ingrediente):
                return False, "Ingrediente já está na composição do produto"
            
            # Create composicao
            composicao = ProdutoIngredientesModel(
                fk_produto=fk_produto,
                fk_ingrediente=fk_ingrediente,
                quantidade_necessaria=qtd
            )
            
            if self.repository.add_ingrediente_ao_produto(composicao):
                return True, "Ingrediente adicionado ao produto com sucesso"
            else:
                return False, "Erro ao adicionar ingrediente ao produto"
        except Exception as e:
            return False, f"Erro ao adicionar composição: {str(e)}"
    
    def get_composicao_produto_view(self, fk_produto: int) -> List[Dict]:
        """Return list of ingredientes in produto with details"""
        return self.repository.get_ingredientes_do_produto(fk_produto)
    
    def update_composicao_qtd(self, fk_produto: int, fk_ingrediente: int, 
                             qtd: float) -> Tuple[bool, str]:
        try:
            # Validate input
            if qtd <= 0:
                return False, "Quantidade deve ser maior que zero"
            
            # Check if composicao exists
            if not self.repository.verificar_ingrediente_no_produto(fk_produto, fk_ingrediente):
                return False, "Ingrediente não encontrado na composição do produto"
            
            # Update quantidade
            if self.repository.update_quantidade_ingrediente_produto(
                fk_produto, fk_ingrediente, qtd):
                return True, "Quantidade atualizada com sucesso"
            else:
                return False, "Erro ao atualizar quantidade"
        except Exception as e:
            return False, f"Erro ao atualizar composição: {str(e)}"
    
    def remove_composicao(self, fk_produto: int, fk_ingrediente: int) -> Tuple[bool, str]:
        try:
            # Check if composicao exists
            if not self.repository.verificar_ingrediente_no_produto(fk_produto, fk_ingrediente):
                return False, "Ingrediente não encontrado na composição do produto"
            
            # Remove composicao
            if self.repository.remove_ingrediente_do_produto(fk_produto, fk_ingrediente):
                return True, "Ingrediente removido da composição com sucesso"
            else:
                return False, "Erro ao remover ingrediente da composição"
        except Exception as e:
            return False, f"Erro ao remover composição: {str(e)}" 