import streamlit as st
import pandas as pd
from typing import List
from Models.produto_ingredientes_model import ProdutoIngredientesModel
from Controller.produto_ingredientes_controller import ProdutoIngredientesController
from Controller.produto_controller import ProdutoController
from Controller.ingrediente_controller import IngredienteController

def show_produto_ingredientes(controller: ProdutoIngredientesController,
                            produto_controller: ProdutoController,
                            ingrediente_controller: IngredienteController):
    st.title("Gerenciamento de Ingredientes por Produto")
    
    # Initialize session state for produto_ingredientes if not exists
    if 'produto_ingredientes' not in st.session_state:
        st.session_state.produto_ingredientes = controller.list_produto_ingredientes()
    
    # Create tabs for different operations
    tab1, tab2, tab3, tab4 = st.tabs(["Criar", "Listar", "Atualizar", "Deletar"])
    
    with tab1:
        st.header("Criar Nova Relação Produto-Ingrediente")
        with st.form("create_produto_ingrediente_form"):
            # Get produtos for selection
            produtos = produto_controller.list_produtos()
            produto_options = {f"{p.nome} (ID: {p.id_produto})": p.id_produto 
                             for p in produtos}
            selected_produto = st.selectbox("Produto", 
                                         options=list(produto_options.keys()))
            
            # Get ingredientes for selection
            ingredientes = ingrediente_controller.list_ingredientes()
            ingrediente_options = {f"{i.nome} (ID: {i.id_ingrediente})": i.id_ingrediente 
                                 for i in ingredientes}
            selected_ingrediente = st.selectbox("Ingrediente", 
                                             options=list(ingrediente_options.keys()))
            
            quantidade = st.number_input("Quantidade", min_value=0.0, step=0.01)
            
            submitted = st.form_submit_button("Criar Relação")
            if submitted:
                produto_id = produto_options[selected_produto]
                ingrediente_id = ingrediente_options[selected_ingrediente]
                success, message = controller.create_produto_ingrediente(produto_id, ingrediente_id, quantidade)
                if success:
                    st.success(message)
                    # Update session state
                    st.session_state.produto_ingredientes = controller.list_produto_ingredientes()
                    st.rerun()
                else:
                    st.error(message)
    
    with tab2:
        st.header("Listar Relações Produto-Ingrediente")
        
        if st.session_state.produto_ingredientes:
            # Convert to DataFrame for better display
            df = [pi.to_dict() for pi in st.session_state.produto_ingredientes]
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhuma relação produto-ingrediente cadastrada")
    
    with tab3:
        st.header("Atualizar Relação Produto-Ingrediente")
        
        # Get all relações for selection
        if st.session_state.produto_ingredientes:
            relacao_options = {f"{pi.produto_nome} - {pi.ingrediente_nome}": pi.id_produto_ingrediente 
                             for pi in st.session_state.produto_ingredientes}
            selected_relacao = st.selectbox("Selecione a relação", 
                                         options=list(relacao_options.keys()))
            
            if selected_relacao:
                relacao_id = relacao_options[selected_relacao]
                relacao = controller.get_produto_ingrediente(relacao_id)
                
                with st.form("update_produto_ingrediente_form"):
                    # Get produtos for selection
                    produtos = produto_controller.list_produtos()
                    produto_options = {f"{p.nome} (ID: {p.id_produto})": p.id_produto 
                                     for p in produtos}
                    selected_produto = st.selectbox("Produto", 
                                                 options=list(produto_options.keys()),
                                                 key="update_produto")
                    
                    # Get ingredientes for selection
                    ingredientes = ingrediente_controller.list_ingredientes()
                    ingrediente_options = {f"{i.nome} (ID: {i.id_ingrediente})": i.id_ingrediente 
                                         for i in ingredientes}
                    selected_ingrediente = st.selectbox("Ingrediente", 
                                                     options=list(ingrediente_options.keys()),
                                                     key="update_ingrediente")
                    
                    quantidade = st.number_input("Quantidade", value=relacao.quantidade, 
                                              min_value=0.0, step=0.01)
                    
                    submitted = st.form_submit_button("Atualizar Relação")
                    if submitted:
                        produto_id = produto_options[selected_produto]
                        ingrediente_id = ingrediente_options[selected_ingrediente]
                        success, message = controller.update_produto_ingrediente_info(relacao_id, 
                                                                                   produto_id, 
                                                                                   ingrediente_id, 
                                                                                   quantidade)
                        if success:
                            st.success(message)
                            # Update session state
                            st.session_state.produto_ingredientes = controller.list_produto_ingredientes()
                            st.rerun()
                        else:
                            st.error(message)
        else:
            st.info("Nenhuma relação produto-ingrediente cadastrada para atualizar")
    
    with tab4:
        st.header("Deletar Relação Produto-Ingrediente")
        
        # Get all relações for selection
        if st.session_state.produto_ingredientes:
            relacao_options = {f"{pi.produto_nome} - {pi.ingrediente_nome}": pi.id_produto_ingrediente 
                             for pi in st.session_state.produto_ingredientes}
            selected_relacao = st.selectbox("Selecione a relação para deletar", 
                                         options=list(relacao_options.keys()),
                                         key="delete_select")
            
            if selected_relacao:
                relacao_id = relacao_options[selected_relacao]
                if st.button("Deletar Relação"):
                    st.warning("Tem certeza que deseja deletar esta relação?")
                    if st.button("Sim, deletar"):
                        success, message = controller.remove_produto_ingrediente(relacao_id)
                        if success:
                            st.success(message)
                            # Update session state
                            st.session_state.produto_ingredientes = controller.list_produto_ingredientes()
                            st.rerun()
                        else:
                            st.error(message)
        else:
            st.info("Nenhuma relação produto-ingrediente cadastrada para deletar")

    st.title("Composição de Produtos (Receitas)")
    
    # Get produtos for dropdown
    produtos = produto_controller.get_produtos_para_display()
    produto_options = {f"{p[0]} - {p[1]}": p[0] for p in produtos}
    
    # Select produto
    produto_selected = st.selectbox("Selecione o Produto", 
                                  options=list(produto_options.keys()))
    fk_produto = produto_options[produto_selected]
    
    # Show current ingredientes
    st.header("Ingredientes Atuais")
    ingredientes = controller.get_composicao_produto_view(fk_produto)
    
    if ingredientes:
        # Create DataFrame for display
        df = pd.DataFrame(ingredientes)
        df['quantidade_necessaria'] = df['quantidade_necessaria'].map('{:.2f}'.format)
        df['unidade'] = df['unidade'].str.strip()
        
        # Add edit and remove buttons
        df['Ações'] = None
        
        # Display table
        st.dataframe(df)
        
        # Edit and remove forms
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Editar Quantidade")
            with st.form("edit_qtd_form"):
                ingrediente_edit = st.selectbox("Selecione o Ingrediente", 
                                              options=[f"{i['id_ingrediente']} - {i['nome_ingrediente']}" 
                                                      for i in ingredientes])
                fk_ingrediente = int(ingrediente_edit.split(' - ')[0])
                
                nova_qtd = st.number_input("Nova Quantidade", min_value=0.1, step=0.1)
                
                submit_edit = st.form_submit_button("Atualizar Quantidade")
                if submit_edit:
                    success, message = controller.update_composicao_qtd(
                        fk_produto, fk_ingrediente, nova_qtd)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        
        with col2:
            st.subheader("Remover Ingrediente")
            with st.form("remove_form"):
                ingrediente_remove = st.selectbox("Selecione o Ingrediente para Remover", 
                                                options=[f"{i['id_ingrediente']} - {i['nome_ingrediente']}" 
                                                        for i in ingredientes])
                fk_ingrediente = int(ingrediente_remove.split(' - ')[0])
                
                submit_remove = st.form_submit_button("Remover Ingrediente")
                if submit_remove:
                    success, message = controller.remove_composicao(
                        fk_produto, fk_ingrediente)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
    else:
        st.info("Nenhum ingrediente cadastrado para este produto.")
    
    # Add new ingrediente
    st.header("Adicionar Novo Ingrediente")
    with st.form("add_ingrediente_form"):
        # Get ingredientes for dropdown
        ingredientes = ingrediente_controller.get_ingredientes_para_display()
        ingrediente_options = {f"{i[0]} - {i[1]} ({i[3]})": i[0] for i in ingredientes}
        
        # Filter out already added ingredientes
        current_ingredientes = [i['id_ingrediente'] for i in controller.get_composicao_produto_view(fk_produto)]
        ingrediente_options = {k: v for k, v in ingrediente_options.items() 
                             if v not in current_ingredientes}
        
        if ingrediente_options:
            ingrediente_selected = st.selectbox("Ingrediente", 
                                              options=list(ingrediente_options.keys()))
            fk_ingrediente = ingrediente_options[ingrediente_selected]
            
            qtd_necessaria = st.number_input("Quantidade Necessária", 
                                           min_value=0.1, step=0.1)
            
            submit_button = st.form_submit_button("Adicionar Ingrediente")
            
            if submit_button:
                success, message = controller.add_composicao(
                    fk_produto=fk_produto,
                    fk_ingrediente=fk_ingrediente,
                    qtd=qtd_necessaria
                )
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        else:
            st.info("Todos os ingredientes já estão na composição deste produto.") 