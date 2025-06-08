from typing import List, Optional, Dict, Tuple
from Models.pedido_venda_model import PedidoVendaModel
from Repository.pedido_venda_repo import PedidoVendaRepository
from Controller.cliente_controller import ClienteController
from Controller.produto_controller import ProdutoController

class PedidoVendaController:
    def __init__(self):
        self.repository = PedidoVendaRepository()
        self.cliente_controller = ClienteController()
        self.produto_controller = ProdutoController()
    
    def create_item_pedido_venda(self, fk_cliente: int, fk_produto: int, 
                                qtd_venda: int) -> Tuple[bool, str]:
        try:
            # Validate input
            if qtd_venda <= 0:
                return False, "Quantidade deve ser maior que zero"
            
            # Check if cliente exists
            cliente = self.cliente_controller.get_cliente(fk_cliente)
            if not cliente:
                return False, "Cliente não encontrado"
            
            # Check if produto exists and has enough stock
            produto = self.produto_controller.get_produto(fk_produto)
            if not produto:
                return False, "Produto não encontrado"
            
            if produto.quantidade < qtd_venda:
                return False, "Estoque insuficiente"
            
            # Create pedido
            pedido = PedidoVendaModel(
                fk_cliente=fk_cliente,
                fk_produto=fk_produto,
                qtd_venda=qtd_venda
            )
            self.repository.add_pedido_venda(pedido)
            
            # Update stock
            success, message = self.produto_controller.ajustar_estoque_produto(
                fk_produto, qtd_venda, 'venda')
            
            if not success:
                # Rollback pedido creation if stock update fails
                self.repository.delete_pedido_venda(pedido.id_pedido_venda)
                return False, f"Erro ao atualizar estoque: {message}"
            
            return True, "Item de pedido criado com sucesso"
        except Exception as e:
            return False, f"Erro ao criar item de pedido: {str(e)}"
    
    def list_itens_pedido_venda_view(self) -> List[Dict]:
        """Return list of pedidos with cliente and produto details"""
        return self.repository.get_all_pedidos_venda_detalhado()
    
    def cancel_item_pedido_venda(self, id_pedido_venda: int) -> Tuple[bool, str]:
        try:
            # Get pedido
            pedido = self.repository.get_pedido_venda_by_id(id_pedido_venda)
            if not pedido:
                return False, "Item de pedido não encontrado"
            
            # Return stock
            success, message = self.produto_controller.ajustar_estoque_produto(
                pedido.fk_produto, pedido.qtd_venda, 'retorno')
            
            if not success:
                return False, f"Erro ao retornar estoque: {message}"
            
            # Delete pedido
            self.repository.delete_pedido_venda(id_pedido_venda)
            return True, "Item de pedido cancelado com sucesso"
        except Exception as e:
            return False, f"Erro ao cancelar item de pedido: {str(e)}"

    def update_item_pedido_venda(self, id_pedido_venda: int, fk_cliente: int, 
                                fk_produto: int, qtd_venda: int) -> Tuple[bool, str]:
        try:
            # Get current pedido
            current_pedido = self.repository.get_pedido_venda_by_id(id_pedido_venda)
            if not current_pedido:
                return False, "Item de pedido não encontrado"
            
            # Validate input
            if qtd_venda <= 0:
                return False, "Quantidade deve ser maior que zero"
            
            # Check if cliente exists
            cliente = self.cliente_controller.get_cliente(fk_cliente)
            if not cliente:
                return False, "Cliente não encontrado"
            
            # Check if produto exists and has enough stock
            produto = self.produto_controller.get_produto(fk_produto)
            if not produto:
                return False, "Produto não encontrado"
            
            # Calculate stock adjustment
            stock_diff = qtd_venda - current_pedido.qtd_venda
            if stock_diff > 0:  # Need to reduce stock
                if produto.quantidade < stock_diff:
                    return False, "Estoque insuficiente"
                success, message = self.produto_controller.ajustar_estoque_produto(
                    fk_produto, stock_diff, 'venda')
            else:  # Need to return stock
                success, message = self.produto_controller.ajustar_estoque_produto(
                    fk_produto, abs(stock_diff), 'retorno')
            
            if not success:
                return False, f"Erro ao atualizar estoque: {message}"
            
            # Update pedido
            pedido = PedidoVendaModel(
                id_pedido_venda=id_pedido_venda,
                fk_cliente=fk_cliente,
                fk_produto=fk_produto,
                qtd_venda=qtd_venda,
                data_venda=current_pedido.data_venda
            )
            self.repository.update_pedido_venda(pedido)
            return True, "Item de pedido atualizado com sucesso"
        except Exception as e:
            return False, f"Erro ao atualizar item de pedido: {str(e)}"

    def get_all_pedidos_venda(self):
        return self.repository.get_all_pedidos_venda()
    
    def get_pedido_venda_by_id(self, id):
        return self.repository.get_pedido_venda_by_id(id)
    
    def create_pedido_venda(self, fk_cliente, fk_funcionario):
        return self.repository.create_pedido_venda(fk_cliente, fk_funcionario)
    
    def update_pedido_venda(self, id, fk_cliente, fk_funcionario):
        return self.repository.update_pedido_venda(id, fk_cliente, fk_funcionario)
    
    def delete_pedido_venda(self, id):
        return self.repository.delete_pedido_venda(id) 