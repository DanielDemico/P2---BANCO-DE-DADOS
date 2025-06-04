import streamlit as st
from Controller.cliente_controller import ClienteController
from Controller.funcionario_controller import FuncionarioController
from Controller.fornecedor_controller import FornecedorController
from Controller.ingrediente_controller import IngredienteController
from Controller.produto_controller import ProdutoController
from Controller.pedido_venda_controller import PedidoVendaController
from Controller.pedido_compra_controller import PedidoCompraController
from Controller.produto_ingredientes_controller import ProdutoIngredientesController
from Views.cliente_view import show_clientes
from Views.funcionario_view import show_funcionarios
from Views.fornecedor_view import show_fornecedores
from Views.ingrediente_view import show_ingredientes
from Views.produto_view import show_produtos
from Views.pedido_venda_view import show_pedidos_venda
from Views.pedido_compra_view import show_pedidos_compra
from Views.produto_ingredientes_view import show_produto_ingredientes

def main():
    st.set_page_config(
        page_title="Sistema Villa",
        page_icon="🏪",
        layout="wide"
    )
    
    # Initialize controllers
    cliente_controller = ClienteController()
    funcionario_controller = FuncionarioController()
    fornecedor_controller = FornecedorController()
    ingrediente_controller = IngredienteController()
    produto_controller = ProdutoController()
    pedido_venda_controller = PedidoVendaController()
    pedido_compra_controller = PedidoCompraController()
    produto_ingredientes_controller = ProdutoIngredientesController()
    
    # Menu lateral
    menu = st.sidebar.selectbox(
        "Menu Principal",
        ["Clientes", "Funcionários", "Fornecedores", "Ingredientes", "Produtos", 
         "Pedidos de Venda", "Pedidos de Compra", "Composição de Produtos"]
    )
    
    # Show selected view
    if menu == "Clientes":
        show_clientes(cliente_controller)
    elif menu == "Funcionários":
        show_funcionarios(funcionario_controller)
    elif menu == "Fornecedores":
        show_fornecedores(fornecedor_controller)
    elif menu == "Ingredientes":
        show_ingredientes(ingrediente_controller, fornecedor_controller)
    elif menu == "Produtos":
        show_produtos(produto_controller)
    elif menu == "Pedidos de Venda":
        show_pedidos_venda(pedido_venda_controller, cliente_controller, produto_controller)
    elif menu == "Pedidos de Compra":
        show_pedidos_compra(pedido_compra_controller, funcionario_controller, ingrediente_controller)
    elif menu == "Composição de Produtos":
        show_produto_ingredientes(produto_ingredientes_controller, produto_controller, ingrediente_controller)

if __name__ == "__main__":
    main() 