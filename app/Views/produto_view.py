import streamlit as st
from typing import List, Tuple
from Models.produto_model import ProdutoModel
from Controller.produto_controller import ProdutoController
from Repository.ingrediente_repo import IngredienteRepository

def show_produtos(controller: ProdutoController):
    st.title("Gerenciamento de Produtos")
    
    # Initialize repositories
    ingrediente_repo = IngredienteRepository()
    
    # Initialize session state for produtos if not exists
    if 'produtos' not in st.session_state:
        st.session_state.produtos = controller.list_produtos()
    
    # Initialize session state for ingredient count if not exists
    if 'ingredientes_count' not in st.session_state:
        st.session_state.ingredientes_count = 0
    
    # Create tabs for different operations
    tab1, tab2, tab3, tab4 = st.tabs(["Criar", "Listar", "Atualizar", "Deletar"])
    
    with tab1:
        st.header("Criar Novo Produto")
        
        # Get all ingredients for selection
        ingredientes = ingrediente_repo.get_all_ingredientes_com_fornecedor()
        if not ingredientes:
            st.error("Não há ingredientes cadastrados. Cadastre ingredientes primeiro.")
            return
        
        # Add ingredient button outside the form
        if st.button("Adicionar Ingrediente"):
            st.session_state.ingredientes_count += 1
            st.rerun()
        
        with st.form("create_produto_form"):
            nome = st.text_input("Nome")
            descricao = st.text_area("Descrição", height=100)
            valor_venda = st.number_input("Valor de Venda", min_value=0.0, step=0.01)
            
            st.subheader("Ingredientes")
            ingredientes_selecionados = []
            
            # Show ingredient inputs
            for i in range(st.session_state.ingredientes_count):
                col1, col2 = st.columns([3, 1])
                with col1:
                    ingrediente_options = {f"{ing['nome_i']} (ID: {ing['id_ingrediente']})": ing['id_ingrediente'] 
                                        for ing in ingredientes}
                    selected = st.selectbox(f"Ingrediente {i+1}", 
                                         options=list(ingrediente_options.keys()),
                                         key=f"ingrediente_{i}")
                    if selected:
                        id_ingrediente = ingrediente_options[selected]
                        with col2:
                            quantidade = st.number_input("Quantidade", min_value=0.0, step=0.1,
                                                      key=f"quantidade_{i}")
                        ingredientes_selecionados.append((id_ingrediente, quantidade))
            
            submitted = st.form_submit_button("Criar Produto")
            if submitted:
                if not ingredientes_selecionados:
                    st.error("Adicione pelo menos um ingrediente ao produto")
                else:
                    success, message = controller.create_produto(nome, descricao, valor_venda, ingredientes_selecionados)
                    if success:
                        st.success(message)
                        # Update session state
                        st.session_state.produtos = controller.list_produtos()
                        st.session_state.ingredientes_count = 0
                        st.rerun()
                    else:
                        st.error(message)
    
    with tab2:
        st.header("Listar Produtos")
        
        if st.session_state.produtos:
            # Convert to DataFrame for better display
            df = [produto.to_dict() for produto in st.session_state.produtos]
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhum produto cadastrado")
    
    with tab3:
        st.header("Atualizar Produto")
        
        # Get all produtos for selection
        if st.session_state.produtos:
            produto_options = {f"{p.nome_p} (ID: {p.id_produto})": p.id_produto 
                             for p in st.session_state.produtos}
            selected_produto = st.selectbox("Selecione o produto", 
                                         options=list(produto_options.keys()))
            
            if selected_produto:
                produto_id = produto_options[selected_produto]
                produto = controller.get_produto(produto_id)
                
                with st.form("update_produto_form"):
                    nome = st.text_input("Nome", value=produto.nome_p)
                    descricao = st.text_area("Descrição", value=produto.descricao, height=100)
                    valor_venda = st.number_input("Valor de Venda", value=produto.valor_venda, 
                                                min_value=0.0, step=0.01)
                    
                    submitted = st.form_submit_button("Atualizar Produto")
                    if submitted:
                        success, message = controller.update_produto_info(produto_id, nome, descricao, valor_venda)
                        if success:
                            st.success(message)
                            # Update session state
                            st.session_state.produtos = controller.list_produtos()
                            st.rerun()
                        else:
                            st.error(message)
        else:
            st.info("Nenhum produto cadastrado para atualizar")
    
    with tab4:
        st.header("Deletar Produto")
        
        # Get all produtos for selection
        if st.session_state.produtos:
            produto_options = {f"{p.nome_p} (ID: {p.id_produto})": p.id_produto 
                             for p in st.session_state.produtos}
            selected_produto = st.selectbox("Selecione o produto para deletar", 
                                         options=list(produto_options.keys()),
                                         key="delete_select")
            
            if selected_produto:
                produto_id = produto_options[selected_produto]
                
                # Initialize confirmation state if not exists
                if 'delete_confirmed' not in st.session_state:
                    st.session_state.delete_confirmed = False
                
                if not st.session_state.delete_confirmed:
                    if st.button("Deletar Produto"):
                        st.warning("Tem certeza que deseja deletar este produto?")
                        st.session_state.delete_confirmed = True
                        st.rerun()
                else:
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Sim, confirmar exclusão"):
                            success, message = controller.remove_produto(produto_id)
                            if success:
                                st.success(message)
                                # Update session state
                                st.session_state.produtos = controller.list_produtos()
                                st.session_state.delete_confirmed = False
                                st.rerun()
                            else:
                                st.error(message)
                                st.session_state.delete_confirmed = False
                    with col2:
                        if st.button("Não, cancelar"):
                            st.session_state.delete_confirmed = False
                            st.rerun()
        else:
            st.info("Nenhum produto cadastrado para deletar") 