import streamlit as st
from typing import List
from Models.fornecedor_model import FornecedorModel
from Controller.fornecedor_controller import FornecedorController

def show_fornecedores(controller: FornecedorController):
    st.title("Gerenciamento de Fornecedores")
    
    # Initialize session state for fornecedores if not exists
    if 'fornecedores' not in st.session_state:
        st.session_state.fornecedores = controller.list_fornecedores()
    
    # Create tabs for different operations
    tab1, tab2, tab3, tab4 = st.tabs(["Criar", "Listar", "Atualizar", "Deletar"])
    
    with tab1:
        st.header("Criar Novo Fornecedor")
        with st.form("create_fornecedor_form"):
            nome = st.text_input("Nome")
            cnpj = st.text_input("CNPJ")
            
            submitted = st.form_submit_button("Criar Fornecedor")
            if submitted:
                success, message = controller.create_fornecedor(nome, cnpj)
                if success:
                    st.success(message)
                    # Update session state
                    st.session_state.fornecedores = controller.list_fornecedores()
                    st.rerun()
                else:
                    st.error(message)
    
    with tab2:
        st.header("Listar Fornecedores")
        
        if st.session_state.fornecedores:
            # Convert to DataFrame for better display
            df = [fornecedor.to_dict() for fornecedor in st.session_state.fornecedores]
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhum fornecedor cadastrado")
    
    with tab3:
        st.header("Atualizar Fornecedor")
        
        # Get all fornecedores for selection
        if st.session_state.fornecedores:
            fornecedor_options = {f"{f.nome} (CNPJ: {f.cnpj})": f.id_fornecedor 
                                for f in st.session_state.fornecedores}
            selected_fornecedor = st.selectbox("Selecione o fornecedor", 
                                            options=list(fornecedor_options.keys()))
            
            if selected_fornecedor:
                fornecedor_id = fornecedor_options[selected_fornecedor]
                fornecedor = controller.get_fornecedor(fornecedor_id)
                
                with st.form("update_fornecedor_form"):
                    nome = st.text_input("Nome", value=fornecedor.nome)
                    
                    submitted = st.form_submit_button("Atualizar Fornecedor")
                    if submitted:
                        success, message = controller.update_fornecedor_info(fornecedor_id, nome)
                        if success:
                            st.success(message)
                            # Update session state
                            st.session_state.fornecedores = controller.list_fornecedores()
                            st.rerun()
                        else:
                            st.error(message)
        else:
            st.info("Nenhum fornecedor cadastrado para atualizar")
    
    with tab4:
        st.header("Deletar Fornecedor")
        
        # Get all fornecedores for selection
        if st.session_state.fornecedores:
            fornecedor_options = {f"{f.nome} (CNPJ: {f.cnpj})": f.id_fornecedor 
                                for f in st.session_state.fornecedores}
            selected_fornecedor = st.selectbox("Selecione o fornecedor para deletar", 
                                            options=list(fornecedor_options.keys()),
                                            key="delete_select")
            
            if selected_fornecedor:
                fornecedor_id = fornecedor_options[selected_fornecedor]
                
                # Initialize confirmation state if not exists
                if 'delete_confirmed' not in st.session_state:
                    st.session_state.delete_confirmed = False
                
                if not st.session_state.delete_confirmed:
                    if st.button("Deletar Fornecedor"):
                        st.warning("Tem certeza que deseja deletar este fornecedor?")
                        st.session_state.delete_confirmed = True
                        st.rerun()
                else:
                    st.warning("Tem certeza que deseja deletar este fornecedor?")
                    if st.button("Sim, deletar"):
                        success, message = controller.remove_fornecedor(fornecedor_id)
                        if success:
                            st.success(message)
                            # Update session state
                            st.session_state.fornecedores = controller.list_fornecedores()
                            st.session_state.delete_confirmed = False
                            st.rerun()
                        else:
                            st.error(message)
                            st.session_state.delete_confirmed = False
        else:
            st.info("Nenhum fornecedor cadastrado para deletar") 