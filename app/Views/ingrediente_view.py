import streamlit as st
from typing import List
from Models.ingrediente_model import IngredienteModel
from Controller.ingrediente_controller import IngredienteController
from Controller.fornecedor_controller import FornecedorController

def show_ingredientes(controller: IngredienteController, fornecedor_controller: FornecedorController):
    st.title("Gerenciamento de Ingredientes")
    
    # Initialize session state for ingredientes if not exists
    if 'ingredientes' not in st.session_state:
        st.session_state.ingredientes = controller.list_ingredientes()
    
    # Create tabs for different operations
    tab1, tab2, tab3, tab4 = st.tabs(["Criar", "Listar", "Atualizar", "Deletar"])
    
    with tab1:
        st.header("Criar Novo Ingrediente")
        with st.form("create_ingrediente_form"):
            nome = st.text_input("Nome")
            valor_compra = st.number_input("Valor de Compra", min_value=0.0, step=0.01)
            quantidade = st.number_input("Quantidade", min_value=0.0, step=0.01)
            
            # Get fornecedores for selection
            fornecedores = fornecedor_controller.list_fornecedores()
            fornecedor_options = {f"{f.nome} (CNPJ: {f.cnpj})": f.id_fornecedor 
                                for f in fornecedores}
            selected_fornecedor = st.selectbox("Fornecedor", 
                                            options=list(fornecedor_options.keys()))
            
            submitted = st.form_submit_button("Criar Ingrediente")
            if submitted:
                fornecedor_id = fornecedor_options[selected_fornecedor]
                success, message = controller.create_ingrediente(nome, valor_compra, quantidade, fornecedor_id)
                if success:
                    st.success(message)
                    # Update session state
                    st.session_state.ingredientes = controller.list_ingredientes()
                    st.rerun()
                else:
                    st.error(message)
    
    with tab2:
        st.header("Listar Ingredientes")
        
        if st.session_state.ingredientes:
            # Convert to DataFrame for better display
            st.dataframe(st.session_state.ingredientes, use_container_width=True)
        else:
            st.info("Nenhum ingrediente cadastrado")
    
    with tab3:
        st.header("Atualizar Ingrediente")
        
        # Get all ingredientes for selection
        if st.session_state.ingredientes:
            ingrediente_options = {f"{i['nome_i']} (ID: {i['id_ingrediente']})": i['id_ingrediente'] 
                                 for i in st.session_state.ingredientes}
            selected_ingrediente = st.selectbox("Selecione o ingrediente", 
                                             options=list(ingrediente_options.keys()))
            
            if selected_ingrediente:
                ingrediente_id = ingrediente_options[selected_ingrediente]
                ingrediente = controller.get_ingrediente_by_id(ingrediente_id)
                
                with st.form("update_ingrediente_form"):
                    nome = st.text_input("Nome", value=ingrediente.nome_i)
                    valor_compra = st.number_input("Valor de Compra", value=ingrediente.valor_compra, 
                                                 min_value=0.0, step=0.01)
                    quantidade = st.number_input("Quantidade", value=ingrediente.quantidade, 
                                              min_value=0.0, step=0.01)
                    
                    # Get fornecedores for selection
                    fornecedores = fornecedor_controller.list_fornecedores()
                    fornecedor_options = {f"{f.nome} (CNPJ: {f.cnpj})": f.id_fornecedor 
                                        for f in fornecedores}
                    selected_fornecedor = st.selectbox("Fornecedor", 
                                                    options=list(fornecedor_options.keys()),
                                                    key="update_fornecedor")
                    
                    submitted = st.form_submit_button("Atualizar Ingrediente")
                    if submitted:
                        fornecedor_id = fornecedor_options[selected_fornecedor]
                        success, message = controller.update_ingrediente(ingrediente_id, nome, 
                                                                       valor_compra, quantidade, 
                                                                       fornecedor_id)
                        if success:
                            st.success(message)
                            # Update session state
                            st.session_state.ingredientes = controller.list_ingredientes()
                            st.rerun()
                        else:
                            st.error(message)
        else:
            st.info("Nenhum ingrediente cadastrado para atualizar")
    
    with tab4:
        st.header("Deletar Ingrediente")
        
        # Get all ingredientes for selection
        if st.session_state.ingredientes:
            ingrediente_options = {f"{i['nome_i']} (ID: {i['id_ingrediente']})": i['id_ingrediente'] 
                                 for i in st.session_state.ingredientes}
            selected_ingrediente = st.selectbox("Selecione o ingrediente para deletar", 
                                             options=list(ingrediente_options.keys()),
                                             key="delete_select")
            
            if selected_ingrediente:
                ingrediente_id = ingrediente_options[selected_ingrediente]
                
                # Initialize confirmation state if not exists
                if 'delete_confirmed' not in st.session_state:
                    st.session_state.delete_confirmed = False
                
                if not st.session_state.delete_confirmed:
                    if st.button("Deletar Ingrediente"):
                        st.warning("Tem certeza que deseja deletar este ingrediente?")
                        st.session_state.delete_confirmed = True
                        st.rerun()
                else:
                    st.warning("Tem certeza que deseja deletar este ingrediente?")
                    if st.button("Sim, deletar"):
                        success, message = controller.remove_ingrediente(ingrediente_id)
                        if success:
                            st.success(message)
                            # Update session state
                            st.session_state.ingredientes = controller.list_ingredientes()
                            st.session_state.delete_confirmed = False
                            st.rerun()
                        else:
                            st.error(message)
                            st.session_state.delete_confirmed = False
        else:
            st.info("Nenhum ingrediente cadastrado para deletar") 