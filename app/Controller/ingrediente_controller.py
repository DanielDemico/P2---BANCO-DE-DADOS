from typing import List, Optional, Dict
from Models.ingrediente_model import IngredienteModel
from Repository.ingrediente_repo import IngredienteRepository
from Controller.fornecedor_controller import FornecedorController

class IngredienteController:
    def __init__(self):
        self.repository = IngredienteRepository()
        self.fornecedor_controller = FornecedorController()
    
    def create_ingrediente(self, nome_i: str, valor_compra: float, 
                         quantidade: int, fk_fornecedor: int) -> tuple[bool, str]:
        try:
            # Validate input
            if not nome_i or not quantidade:
                return False, "Nome e Quantidade são obrigatórios"
            
            if valor_compra <= 0:
                return False, "Valor de compra deve ser maior que zero"
            
            # Check if fornecedor exists
            fornecedor = self.fornecedor_controller.get_fornecedor(fk_fornecedor)
            if not fornecedor:
                return False, "Fornecedor não encontrado"
            
            # Create and save ingrediente
            ingrediente = IngredienteModel(
                nome_i=nome_i,
                valor_compra=valor_compra,
                quantidade=quantidade,
                fk_fornecedor=fk_fornecedor
            )
            self.repository.add_ingrediente(ingrediente)
            return True, "Ingrediente cadastrado com sucesso"
        except Exception as e:
            return False, str(e)
    
    def list_ingredientes(self) -> List[Dict]:
        """Return list of ingredientes with fornecedor names"""
        return self.repository.get_all_ingredientes_com_fornecedor()
    
    def get_ingrediente_by_id(self, id_ingrediente: int) -> Optional[IngredienteModel]:
        return self.repository.get_ingrediente_by_id(id_ingrediente)
    
    def update_ingrediente(self, id_ingrediente: int, nome_i: str, 
                         valor_compra: float, quantidade: str, 
                         fk_fornecedor: int) -> tuple[bool, str]:
        try:
            # Validate input
            if not nome_i or not quantidade:
                return False, "Nome e quantidade são obrigatórios"
            
            if valor_compra <= 0:
                return False, "Valor de compra deve ser maior que zero"
            
            # Check if ingrediente exists
            ingrediente = self.repository.get_ingrediente_by_id(id_ingrediente)
            if not ingrediente:
                return False, "Ingrediente não encontrado"
            
            # Check if fornecedor exists
            fornecedor = self.fornecedor_controller.get_fornecedor(fk_fornecedor)
            if not fornecedor:
                return False, "Fornecedor não encontrado"
            
            # Update ingrediente
            updated_ingrediente = IngredienteModel(
                id_ingrediente=id_ingrediente,
                nome_i=nome_i,
                valor_compra=valor_compra,
                quantidade=quantidade,
                fk_fornecedor=fk_fornecedor
            )
            self.repository.update_ingrediente(id_ingrediente, updated_ingrediente)
            return True, "Ingrediente atualizado com sucesso"
        except Exception as e:
            return False, str(e)
    
    def remove_ingrediente(self, id_ingrediente: int) -> tuple[bool, str]:
        try:
            # Check if ingrediente exists
            ingrediente = self.repository.get_ingrediente_by_id(id_ingrediente)
            if not ingrediente:
                return False, "Ingrediente não encontrado"
            
            # Check for dependencies
            if self.repository.check_dependencies(id_ingrediente):
                return False, "Não é possível remover este ingrediente pois ele está sendo usado em pedidos ou produtos"
            
            # Remove ingrediente
            self.repository.delete_ingrediente(id_ingrediente)
            return True, "Ingrediente removido com sucesso"
        except Exception as e:
            return False, str(e) 