import streamlit as st
from typing import List
from Models.funcionario_model import FuncionarioModel
from Controller.funcionario_controller import FuncionarioController
from datetime import date, datetime

def show_funcionarios(controller: FuncionarioController):
    st.title("Gerenciamento de Funcionários")
    
    # Initialize session state for funcionarios if not exists
    if 'funcionarios' not in st.session_state:
        st.session_state.funcionarios = controller.list_funcionarios()
    
    # Create tabs for different operations
    tab1, tab2, tab3, tab4 = st.tabs(["Criar", "Listar", "Atualizar", "Deletar"])
    
    with tab1:
        st.header("Criar Novo Funcionário")
        with st.form("create_funcionario_form"):
            nome = st.text_input("Nome")
            dt_nascimento_str = st.text_input("Data de Nascimento (DD/MM/AAAA)")
            cpf = st.text_input("CPF")
            
            submitted = st.form_submit_button("Criar Funcionário")
            if submitted:
                try:
                    dt_nascimento = datetime.strptime(dt_nascimento_str, "%d/%m/%Y").date()
                    success, message = controller.create_funcionario(nome, dt_nascimento, cpf)
                    if success:
                        st.success(message)
                        # Update session state
                        st.session_state.funcionarios = controller.list_funcionarios()
                        st.rerun()
                    else:
                        st.error(message)
                except ValueError:
                    st.error("Formato de data inválido. Use DD/MM/AAAA")
    
    with tab2:
        st.header("Listar Funcionários")
        
        if st.session_state.funcionarios:
            # Convert to DataFrame for better display
            df = [funcionario.to_dict() for funcionario in st.session_state.funcionarios]
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhum funcionário cadastrado")
    
    with tab3:
        st.header("Atualizar Funcionário")
        
        # Get all funcionarios for selection
        if st.session_state.funcionarios:
            funcionario_options = {f"{f.nome} (CPF: {f.cpf})": f.id_funcionario 
                                 for f in st.session_state.funcionarios}
            selected_funcionario = st.selectbox("Selecione o funcionário", 
                                             options=list(funcionario_options.keys()))
            
            if selected_funcionario:
                funcionario_id = funcionario_options[selected_funcionario]
                funcionario = controller.get_funcionario(funcionario_id)
                
                with st.form("update_funcionario_form"):
                    nome = st.text_input("Nome", value=funcionario.nome)
                    dt_nascimento_str = st.text_input("Data de Nascimento (DD/MM/AAAA)", 
                                                    value=funcionario.dt_nascimento.strftime("%d/%m/%Y"))
                    
                    submitted = st.form_submit_button("Atualizar Funcionário")
                    if submitted:
                        try:
                            dt_nascimento = datetime.strptime(dt_nascimento_str, "%d/%m/%Y").date()
                            success, message = controller.update_funcionario_info(funcionario_id, nome, dt_nascimento)
                            if success:
                                st.success(message)
                                # Update session state
                                st.session_state.funcionarios = controller.list_funcionarios()
                                st.rerun()
                            else:
                                st.error(message)
                        except ValueError:
                            st.error("Formato de data inválido. Use DD/MM/AAAA")
        else:
            st.info("Nenhum funcionário cadastrado para atualizar")
    
    with tab4:
        st.header("Deletar Funcionário")
        
        # Get all funcionarios for selection
        if st.session_state.funcionarios:
            funcionario_options = {f"{f.nome} (CPF: {f.cpf})": f.id_funcionario 
                                 for f in st.session_state.funcionarios}
            selected_funcionario = st.selectbox("Selecione o funcionário para deletar", 
                                             options=list(funcionario_options.keys()),
                                             key="delete_select")
            
            if selected_funcionario:
                funcionario_id = funcionario_options[selected_funcionario]
                
                # Initialize confirmation state if not exists
                if 'delete_confirmed' not in st.session_state:
                    st.session_state.delete_confirmed = False
                
                if not st.session_state.delete_confirmed:
                    if st.button("Deletar Funcionário"):
                        st.warning("Tem certeza que deseja deletar este funcionário?")
                        st.session_state.delete_confirmed = True
                        st.rerun()
                else:
                    st.warning("Tem certeza que deseja deletar este funcionário?")
                    if st.button("Sim, deletar"):
                        success, message = controller.remove_funcionario(funcionario_id)
                        if success:
                            st.success(message)
                            # Update session state
                            st.session_state.funcionarios = controller.list_funcionarios()
                            st.session_state.delete_confirmed = False
                            st.rerun()
                        else:
                            st.error(message)
                            st.session_state.delete_confirmed = False
        else:
            st.info("Nenhum funcionário cadastrado para deletar") 