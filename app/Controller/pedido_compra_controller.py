from typing import List, Optional, Dict, Tuple
from Models.pedido_compra_model import PedidoCompraModel
from Repository.pedido_compra_repo import PedidoCompraRepository
from Controller.funcionario_controller import FuncionarioController
from Controller.ingrediente_controller import IngredienteController

class PedidoCompraController:
    def __init__(self):
        self.repository = PedidoCompraRepository()
        self.funcionario_controller = FuncionarioController()
        self.ingrediente_controller = IngredienteController()
    
    def create_item_pedido_compra(self, fk_funcionario: int, fk_ingrediente: int, 
                                 qtd_ingrediente: float) -> Tuple[bool, str]:
        try:
            # Validate input
            if qtd_ingrediente <= 0:
                return False, "Quantidade deve ser maior que zero"
            
            # Check if funcionario exists
            funcionario = self.funcionario_controller.get_funcionario(fk_funcionario)
            if not funcionario:
                return False, "Funcionário não encontrado"
            
            # Check if ingrediente exists
            ingrediente = self.ingrediente_controller.get_ingrediente_by_id(fk_ingrediente)
            if not ingrediente:
                return False, "Ingrediente não encontrado"
            
            # Create pedido
            pedido = PedidoCompraModel(
                fk_funcionario=fk_funcionario,
                fk_ingrediente=fk_ingrediente,
                qtd_ingrediente=qtd_ingrediente
            )
            self.repository.add_pedido_compra(pedido)
            
            return True, "Item de pedido de compra criado com sucesso"
        except Exception as e:
            return False, f"Erro ao criar item de pedido: {str(e)}"
    
    def list_itens_pedido_compra_view(self) -> List[Dict]:
        """Return list of pedidos with funcionario and ingrediente details"""
        return self.repository.get_all_pedidos_compra_detalhado()
    
    def update_status_item_pedido_compra(self, id_pedido_compra: int, status: str) -> Tuple[bool, str]:
        try:
            # Get pedido
            pedido = self.repository.get_pedido_compra_by_id(id_pedido_compra)
            if not pedido:
                return False, "Item de pedido não encontrado"
            
            # Update status
            self.repository.update_pedido_compra_status(id_pedido_compra, status)
            
            # If status is "Recebido", update ingrediente stock
            if status.lower() == "recebido":
                success, message = self.ingrediente_controller.ajustar_estoque_ingrediente(
                    pedido.fk_ingrediente, pedido.qtd_ingrediente, 'entrada')
                if not success:
                    return False, f"Erro ao atualizar estoque: {message}"
            
            return True, "Status do item de pedido atualizado com sucesso"
        except Exception as e:
            return False, f"Erro ao atualizar status: {str(e)}"
    
    def remove_item_pedido_compra(self, id_pedido_compra: int) -> Tuple[bool, str]:
        try:
            # Get pedido
            pedido = self.repository.get_pedido_compra_by_id(id_pedido_compra)
            if not pedido:
                return False, "Item de pedido não encontrado"
            
            # Delete pedido
            self.repository.delete_pedido_compra(id_pedido_compra)
            return True, "Item de pedido removido com sucesso"
        except Exception as e:
            return False, f"Erro ao remover item de pedido: {str(e)}"

    def get_all_pedidos_compra(self):
        return self.repository.get_all_pedidos_compra()
    
    def get_pedido_compra_by_id(self, id):
        return self.repository.get_pedido_compra_by_id(id)
    
    def create_pedido_compra(self, fk_fornecedor, fk_ingredientes):
        return self.repository.create_pedido_compra(fk_fornecedor, fk_ingredientes)
    
    def update_pedido_compra(self, id, fk_fornecedor, fk_ingredientes):
        return self.repository.update_pedido_compra(id, fk_fornecedor, fk_ingredientes)
    
    def delete_pedido_compra(self, id):
        return self.repository.delete_pedido_compra(id) 