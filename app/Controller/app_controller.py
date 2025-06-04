import streamlit as st
from Views.main_view import MainView
from Controller.cliente_controller import ClienteController
from Controller.fornecedor_controller import FornecedorController
from Controller.funcionario_controller import FuncionarioController
from Controller.ingrediente_controller import IngredienteController
from Controller.produto_controller import ProdutoController
from Controller.pedido_compra_controller import PedidoCompraController
from Controller.pedido_venda_controller import PedidoVendaController

class AppController:
    def __init__(self):
        # Inicializa os controllers
        self.cliente_controller = ClienteController()
        self.fornecedor_controller = FornecedorController()
        self.funcionario_controller = FuncionarioController()
        self.ingrediente_controller = IngredienteController()
        self.produto_controller = ProdutoController()
        self.pedido_compra_controller = PedidoCompraController()
        self.pedido_venda_controller = PedidoVendaController()
        
        # Inicializa a view
        self.view = MainView()
        
    def run(self):
        st.title("Sistema Villa")
        
        # Menu lateral
        menu = st.sidebar.selectbox(
            "Menu Principal",
            ["Clientes", "Fornecedores", "Funcionários", "Ingredientes", 
             "Produtos", "Pedidos de Compra", "Pedidos de Venda"]
        )
        
        # Renderiza a página apropriada
        if menu == "Clientes":
            self.view.show_clientes(self.cliente_controller)
        elif menu == "Fornecedores":
            self.view.show_fornecedores(self.fornecedor_controller)
        elif menu == "Funcionários":
            self.view.show_funcionarios(self.funcionario_controller)
        elif menu == "Ingredientes":
            self.view.show_ingredientes(self.ingrediente_controller)
        elif menu == "Produtos":
            self.view.show_produtos(self.produto_controller)
        elif menu == "Pedidos de Compra":
            self.view.show_pedidos_compra(self.pedido_compra_controller)
        elif menu == "Pedidos de Venda":
            self.view.show_pedidos_venda(self.pedido_venda_controller) 