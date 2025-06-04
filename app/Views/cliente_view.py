import streamlit as st
from typing import List
from Models.cliente_model import ClienteModel
from Controller.cliente_controller import ClienteController

def show_clientes(controller: ClienteController):
    st.title("Gerenciamento de Clientes")
    
    # Initialize session state for clientes if not exists
    if 'clientes' not in st.session_state:
        st.session_state.clientes = controller.list_clientes()
    
    # Create tabs for different operations
    tab1, tab2, tab3, tab4 = st.tabs(["Criar", "Listar", "Atualizar", "Deletar"])
    
    with tab1:
        st.header("Criar Novo Cliente")
        with st.form("create_cliente_form"):
            nome = st.text_input("Nome")
            mesa = st.number_input("Mesa", min_value=1, step=1)
            cpf = st.text_input("CPF")
            
            submitted = st.form_submit_button("Criar Cliente")
            if submitted:
                success, message = controller.create_cliente(nome, mesa, cpf)
                if success:
                    st.success(message)
                    # Update session state
                    st.session_state.clientes = controller.list_clientes()
                    st.rerun()
                else:
                    st.error(message)
    
    with tab2:
        st.header("Listar Clientes")
        
        if st.session_state.clientes:
            # Convert to DataFrame for better display
            df = [cliente.to_dict() for cliente in st.session_state.clientes]
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhum cliente cadastrado")
    
    with tab3:
        st.header("Atualizar Cliente")
        
        # Get all clientes for selection
        if st.session_state.clientes:
            cliente_options = {f"{c.nome} (CPF: {c.cpf})": c.id_cliente 
                             for c in st.session_state.clientes}
            selected_cliente = st.selectbox("Selecione o cliente", 
                                         options=list(cliente_options.keys()))
            
            if selected_cliente:
                cliente_id = cliente_options[selected_cliente]
                cliente = controller.get_cliente(cliente_id)
                
                with st.form("update_cliente_form"):
                    nome = st.text_input("Nome", value=cliente.nome)
                    mesa = st.number_input("Mesa", value=cliente.mesa, min_value=1, step=1)
                    
                    submitted = st.form_submit_button("Atualizar Cliente")
                    if submitted:
                        success, message = controller.update_cliente_info(cliente_id, nome, mesa)
                        if success:
                            st.success(message)
                            # Update session state
                            st.session_state.clientes = controller.list_clientes()
                            st.rerun()
                        else:
                            st.error(message)
        else:
            st.info("Nenhum cliente cadastrado para atualizar")
    
    with tab4:
        st.header("Deletar Cliente")
        
        # Get all clientes for selection
        if st.session_state.clientes:
            cliente_options = {f"{c.nome} (CPF: {c.cpf})": c.id_cliente 
                             for c in st.session_state.clientes}
            selected_cliente = st.selectbox("Selecione o cliente para deletar", 
                                         options=list(cliente_options.keys()),
                                         key="delete_select")
            
            if selected_cliente:
                cliente_id = cliente_options[selected_cliente]
                
                # Initialize confirmation state if not exists
                if 'delete_confirmed' not in st.session_state:
                    st.session_state.delete_confirmed = False
                
                if not st.session_state.delete_confirmed:
                    if st.button("Deletar Cliente"):
                        st.warning("Tem certeza que deseja deletar este cliente?")
                        st.session_state.delete_confirmed = True
                        st.rerun()
                else:
                    st.warning("Tem certeza que deseja deletar este cliente?")
                    if st.button("Sim, deletar"):
                        success, message = controller.remove_cliente(cliente_id)
                        if success:
                            st.success(message)
                            # Update session state
                            st.session_state.clientes = controller.list_clientes()
                            st.session_state.delete_confirmed = False
                            st.rerun()
                        else:
                            st.error(message)
                            st.session_state.delete_confirmed = False
        else:
            st.info("Nenhum cliente cadastrado para deletar") 