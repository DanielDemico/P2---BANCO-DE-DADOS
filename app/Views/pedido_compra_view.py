import streamlit as st
import pandas as pd
from typing import List
from Models.pedido_compra_model import PedidoCompraModel
from Controller.pedido_compra_controller import PedidoCompraController
from Controller.funcionario_controller import FuncionarioController
from Controller.ingrediente_controller import IngredienteController
from Controller.fornecedor_controller import FornecedorController

def show_pedidos_compra(controller: PedidoCompraController, 
                       funcionario_controller: FuncionarioController,
                       ingrediente_controller: IngredienteController,
                       fornecedor_controller: FornecedorController):
    st.title("Gerenciamento de Pedidos de Compra")
    
    # Initialize session state for pedidos if not exists
    if 'pedidos_compra' not in st.session_state:
        st.session_state.pedidos_compra = controller.get_all_pedidos_compra()
    
    # Create tabs for different operations
    tab1, tab2, tab3, tab4 = st.tabs(["Criar", "Listar", "Atualizar", "Deletar"])
    
    with tab1:
        st.header("Criar Novo Pedido de Compra")
        with st.form("create_pedido_compra_form"):
            # Get fornecedores for selection
            fornecedores = fornecedor_controller.list_fornecedores()
            fornecedor_options = {f"{f.nome} (CNPJ: {f.cnpj})": f.id_fornecedor 
                                for f in fornecedores}
            selected_fornecedor = st.selectbox("Fornecedor", 
                                            options=list(fornecedor_options.keys()))
            
            # Get ingredientes for selection
            ingredientes = ingrediente_controller.list_ingredientes()
            ingrediente_options = {f"{i['nome_i']} (ID: {i['id_ingrediente']})": i['id_ingrediente'] 
                                 for i in ingredientes}
            selected_ingrediente = st.selectbox("Ingrediente", 
                                             options=list(ingrediente_options.keys()))
            
            quantidade = st.number_input("Quantidade", min_value=1.0, step=0.1)
            
            submitted = st.form_submit_button("Criar Pedido de Compra")
            if submitted:
                fornecedor_id = fornecedor_options[selected_fornecedor]
                ingrediente_id = ingrediente_options[selected_ingrediente]
                success, message = controller.create_item_pedido_compra(fornecedor_id, ingrediente_id, quantidade)
                if success:
                    st.success(message)
                    # Update session state
                    st.session_state.pedidos_compra = controller.get_all_pedidos_compra()
                    st.rerun()
                else:
                    st.error(message)
    
    with tab2:
        st.header("Listar Pedidos de Compra")
        
        if st.session_state.pedidos_compra:
            # Convert to DataFrame for better display
            df = [pedido.to_dict() for pedido in st.session_state.pedidos_compra]
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhum pedido de compra cadastrado")
    
    with tab3:
        st.header("Atualizar Pedido de Compra")
        
        # Get all pedidos for selection
        if st.session_state.pedidos_compra:
            pedido_options = {f"Pedido {p.id_pedido_compra} - {p.data_compra}": p.id_pedido_compra 
                            for p in st.session_state.pedidos_compra}
            selected_pedido = st.selectbox("Selecione o pedido", 
                                        options=list(pedido_options.keys()))
            
            if selected_pedido:
                pedido_id = pedido_options[selected_pedido]
                pedido = controller.get_pedido_compra_by_id(pedido_id)
                
                with st.form("update_pedido_compra_form"):
                    # Get fornecedores for selection
                    fornecedores = fornecedor_controller.list_fornecedores()
                    fornecedor_options = {f"{f.nome} (CNPJ: {f.cnpj})": f.id_fornecedor 
                                        for f in fornecedores}
                    selected_fornecedor = st.selectbox("Fornecedor", 
                                                    options=list(fornecedor_options.keys()),
                                                    key="update_fornecedor")
                    
                    # Get ingredientes for selection
                    ingredientes = ingrediente_controller.list_ingredientes()
                    ingrediente_options = {f"{i['nome_i']} (ID: {i['id_ingrediente']})": i['id_ingrediente'] 
                                         for i in ingredientes}
                    selected_ingrediente = st.selectbox("Ingrediente", 
                                                     options=list(ingrediente_options.keys()),
                                                     key="update_ingrediente")
                    
                    quantidade = st.number_input("Quantidade", value=pedido.qtd_ingrediente, 
                                              min_value=1.0, step=0.1)
                    
                    submitted = st.form_submit_button("Atualizar Pedido de Compra")
                    if submitted:
                        fornecedor_id = fornecedor_options[selected_fornecedor]
                        ingrediente_id = ingrediente_options[selected_ingrediente]
                        success, message = controller.update_pedido_info(pedido_id, fornecedor_id, 
                                                                      ingrediente_id, quantidade)
                        if success:
                            st.success(message)
                            # Update session state
                            st.session_state.pedidos_compra = controller.get_all_pedidos_compra()
                            st.rerun()
                        else:
                            st.error(message)
        else:
            st.info("Nenhum pedido de compra cadastrado para atualizar")
    
    with tab4:
        st.header("Deletar Pedido de Compra")
        
        # Get all pedidos for selection
        if st.session_state.pedidos_compra:
            pedido_options = {f"Pedido {p.id_pedido_compra} - {p.data_compra}": p.id_pedido_compra 
                            for p in st.session_state.pedidos_compra}
            selected_pedido = st.selectbox("Selecione o pedido para deletar", 
                                        options=list(pedido_options.keys()),
                                        key="delete_select")
            
            if selected_pedido:
                pedido_id = pedido_options[selected_pedido]
                
                # Initialize confirmation state if not exists
                if 'delete_confirmed' not in st.session_state:
                    st.session_state.delete_confirmed = False
                
                if not st.session_state.delete_confirmed:
                    if st.button("Deletar Pedido"):
                        st.warning("Tem certeza que deseja deletar este pedido?")
                        if st.button("Sim, deletar"):
                            st.session_state.delete_confirmed = True
                            st.rerun()
                else:
                    success, message = controller.remove_pedido(pedido_id)
                    if success:
                        st.success(message)
                        # Update session state
                        st.session_state.pedidos_compra = controller.get_all_pedidos_compra()
                        st.session_state.delete_confirmed = False
                        st.rerun()
                    else:
                        st.error(message)
                        st.session_state.delete_confirmed = False
        else:
            st.info("Nenhum pedido cadastrado para deletar") 