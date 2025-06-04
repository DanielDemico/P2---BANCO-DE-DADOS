import streamlit as st
from typing import List
from Models.pedido_venda_model import PedidoVendaModel
from Controller.pedido_venda_controller import PedidoVendaController
from Controller.cliente_controller import ClienteController
from Controller.produto_controller import ProdutoController

def show_pedidos_venda(controller: PedidoVendaController, 
                      cliente_controller: ClienteController,
                      produto_controller: ProdutoController):
    st.title("Gerenciamento de Pedidos de Venda")
    
    # Initialize session state for pedidos if not exists
    if 'pedidos_venda' not in st.session_state:
        st.session_state.pedidos_venda = controller.list_pedidos()
    
    # Create tabs for different operations
    tab1, tab2, tab3, tab4 = st.tabs(["Criar", "Listar", "Atualizar", "Deletar"])
    
    with tab1:
        st.header("Criar Novo Pedido de Venda")
        with st.form("create_pedido_venda_form"):
            # Get clientes for selection
            clientes = cliente_controller.list_clientes()
            cliente_options = {f"{c.nome} (CPF: {c.cpf})": c.id_cliente 
                             for c in clientes}
            selected_cliente = st.selectbox("Cliente", 
                                         options=list(cliente_options.keys()))
            
            # Get produtos for selection
            produtos = produto_controller.list_produtos()
            produto_options = {f"{p.nome} (ID: {p.id_produto})": p.id_produto 
                             for p in produtos}
            selected_produto = st.selectbox("Produto", 
                                         options=list(produto_options.keys()))
            
            quantidade = st.number_input("Quantidade", min_value=1, step=1)
            
            submitted = st.form_submit_button("Criar Pedido de Venda")
            if submitted:
                cliente_id = cliente_options[selected_cliente]
                produto_id = produto_options[selected_produto]
                success, message = controller.create_pedido(cliente_id, produto_id, quantidade)
                if success:
                    st.success(message)
                    # Update session state
                    st.session_state.pedidos_venda = controller.list_pedidos()
                    st.rerun()
                else:
                    st.error(message)
    
    with tab2:
        st.header("Listar Pedidos de Venda")
        
        if st.session_state.pedidos_venda:
            # Convert to DataFrame for better display
            df = [pedido.to_dict() for pedido in st.session_state.pedidos_venda]
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhum pedido de venda cadastrado")
    
    with tab3:
        st.header("Atualizar Pedido de Venda")
        
        # Get all pedidos for selection
        if st.session_state.pedidos_venda:
            pedido_options = {f"Pedido {p.id_pedido} - {p.data_pedido}": p.id_pedido 
                            for p in st.session_state.pedidos_venda}
            selected_pedido = st.selectbox("Selecione o pedido", 
                                        options=list(pedido_options.keys()))
            
            if selected_pedido:
                pedido_id = pedido_options[selected_pedido]
                pedido = controller.get_pedido(pedido_id)
                
                with st.form("update_pedido_venda_form"):
                    # Get clientes for selection
                    clientes = cliente_controller.list_clientes()
                    cliente_options = {f"{c.nome} (CPF: {c.cpf})": c.id_cliente 
                                     for c in clientes}
                    selected_cliente = st.selectbox("Cliente", 
                                                 options=list(cliente_options.keys()),
                                                 key="update_cliente")
                    
                    # Get produtos for selection
                    produtos = produto_controller.list_produtos()
                    produto_options = {f"{p.nome} (ID: {p.id_produto})": p.id_produto 
                                     for p in produtos}
                    selected_produto = st.selectbox("Produto", 
                                                 options=list(produto_options.keys()),
                                                 key="update_produto")
                    
                    quantidade = st.number_input("Quantidade", value=pedido.quantidade, 
                                              min_value=1, step=1)
                    
                    submitted = st.form_submit_button("Atualizar Pedido de Venda")
                    if submitted:
                        cliente_id = cliente_options[selected_cliente]
                        produto_id = produto_options[selected_produto]
                        success, message = controller.update_pedido_info(pedido_id, cliente_id, 
                                                                      produto_id, quantidade)
                        if success:
                            st.success(message)
                            # Update session state
                            st.session_state.pedidos_venda = controller.list_pedidos()
                            st.rerun()
                        else:
                            st.error(message)
        else:
            st.info("Nenhum pedido de venda cadastrado para atualizar")
    
    with tab4:
        st.header("Deletar Pedido de Venda")
        
        # Get all pedidos for selection
        if st.session_state.pedidos_venda:
            pedido_options = {f"Pedido {p.id_pedido} - {p.cliente.nome}": p.id_pedido 
                            for p in st.session_state.pedidos_venda}
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
                        st.session_state.pedidos_venda = controller.list_pedidos()
                        st.session_state.delete_confirmed = False
                        st.rerun()
                    else:
                        st.error(message)
                        st.session_state.delete_confirmed = False
        else:
            st.info("Nenhum pedido cadastrado para deletar") 