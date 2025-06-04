import streamlit as st

class MainView:
    def show_clientes(self, model):
        st.header("Gerenciamento de Clientes")
        
        # Abas para diferentes operações
        tab1, tab2, tab3 = st.tabs(["Listar", "Adicionar", "Editar/Excluir"])
        
        with tab1:
            st.subheader("Lista de Clientes")
            clientes = model.get_all_clientes()
            if clientes:
                st.dataframe(clientes, column_config={
                    "id_cliente": "ID",
                    "nome": "Nome",
                    "CPF": "CPF",
                    "mesa": "Mesa",
                    "fk_pedido_venda": "Pedido Venda"
                })
            else:
                st.info("Nenhum cliente cadastrado.")
        
        with tab2:
            st.subheader("Novo Cliente")
            with st.form("novo_cliente"):
                nome = st.text_input("Nome")
                cpf = st.text_input("CPF")
                mesa = st.text_input("Mesa")
                fk_pedido_venda = st.number_input("ID do Pedido de Venda", min_value=1)
                
                if st.form_submit_button("Cadastrar"):
                    if nome and cpf and mesa and fk_pedido_venda:
                        model.create_cliente(nome, cpf, mesa, fk_pedido_venda)
                        st.success("Cliente cadastrado com sucesso!")
                    else:
                        st.error("Preencha todos os campos!")
        
        with tab3:
            st.subheader("Editar/Excluir Cliente")
            clientes = model.get_all_clientes()
            if clientes:
                cliente_id = st.selectbox(
                    "Selecione o cliente",
                    options=[c[0] for c in clientes],
                    format_func=lambda x: f"ID: {x}"
                )
                
                if cliente_id:
                    cliente = model.get_cliente_by_id(cliente_id)
                    if cliente:
                        with st.form("editar_cliente"):
                            nome = st.text_input("Nome", value=cliente[1])
                            cpf = st.text_input("CPF", value=cliente[2])
                            mesa = st.text_input("Mesa", value=cliente[3])
                            fk_pedido_venda = st.number_input("ID do Pedido de Venda", value=cliente[4])
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button("Atualizar"):
                                    model.update_cliente(cliente_id, nome, cpf, mesa, fk_pedido_venda)
                                    st.success("Cliente atualizado com sucesso!")
                            with col2:
                                if st.form_submit_button("Excluir"):
                                    model.delete_cliente(cliente_id)
                                    st.success("Cliente excluído com sucesso!")
            else:
                st.info("Nenhum cliente cadastrado.")
    
    def show_fornecedores(self, model):
        st.header("Gerenciamento de Fornecedores")
        
        tab1, tab2, tab3 = st.tabs(["Listar", "Adicionar", "Editar/Excluir"])
        
        with tab1:
            st.subheader("Lista de Fornecedores")
            fornecedores = model.get_all_fornecedores()
            if fornecedores:
                st.dataframe(fornecedores, column_config={
                    "id_fornecedores": "ID",
                    "CNPJ": "CNPJ",
                    "fk_pedido_compra": "Pedido Compra",
                    "fk_ingredientes": "Ingrediente"
                })
            else:
                st.info("Nenhum fornecedor cadastrado.")
        
        with tab2:
            st.subheader("Novo Fornecedor")
            with st.form("novo_fornecedor"):
                cnpj = st.text_input("CNPJ")
                fk_pedido_compra = st.number_input("ID do Pedido de Compra", min_value=1)
                fk_ingredientes = st.number_input("ID do Ingrediente", min_value=1)
                
                if st.form_submit_button("Cadastrar"):
                    if cnpj and fk_pedido_compra and fk_ingredientes:
                        model.create_fornecedor(cnpj, fk_pedido_compra, fk_ingredientes)
                        st.success("Fornecedor cadastrado com sucesso!")
                    else:
                        st.error("Preencha todos os campos!")
        
        with tab3:
            st.subheader("Editar/Excluir Fornecedor")
            fornecedores = model.get_all_fornecedores()
            if fornecedores:
                fornecedor_id = st.selectbox(
                    "Selecione o fornecedor",
                    options=[f[0] for f in fornecedores],
                    format_func=lambda x: f"ID: {x}"
                )
                
                if fornecedor_id:
                    fornecedor = model.get_fornecedor_by_id(fornecedor_id)
                    if fornecedor:
                        with st.form("editar_fornecedor"):
                            cnpj = st.text_input("CNPJ", value=fornecedor[1])
                            fk_pedido_compra = st.number_input("ID do Pedido de Compra", value=fornecedor[2])
                            fk_ingredientes = st.number_input("ID do Ingrediente", value=fornecedor[3])
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button("Atualizar"):
                                    model.update_fornecedor(fornecedor_id, cnpj, fk_pedido_compra, fk_ingredientes)
                                    st.success("Fornecedor atualizado com sucesso!")
                            with col2:
                                if st.form_submit_button("Excluir"):
                                    model.delete_fornecedor(fornecedor_id)
                                    st.success("Fornecedor excluído com sucesso!")
            else:
                st.info("Nenhum fornecedor cadastrado.")
    
    def show_funcionarios(self, model):
        st.header("Gerenciamento de Funcionários")
        
        tab1, tab2, tab3 = st.tabs(["Listar", "Adicionar", "Editar/Excluir"])
        
        with tab1:
            st.subheader("Lista de Funcionários")
            funcionarios = model.get_all_funcionarios()
            if funcionarios:
                st.dataframe(funcionarios, column_config={
                    "id_funcionario": "ID",
                    "nome": "Nome",
                    "fk_cliente": "Cliente",
                    "fk_pedido_compra": "Pedido Compra",
                    "fk_pedido_venda": "Pedido Venda"
                })
            else:
                st.info("Nenhum funcionário cadastrado.")
        
        with tab2:
            st.subheader("Novo Funcionário")
            with st.form("novo_funcionario"):
                nome = st.text_input("Nome")
                fk_cliente = st.number_input("ID do Cliente", min_value=1)
                fk_pedido_compra = st.number_input("ID do Pedido de Compra", min_value=1)
                fk_pedido_venda = st.number_input("ID do Pedido de Venda", min_value=1)
                
                if st.form_submit_button("Cadastrar"):
                    if nome and fk_cliente and fk_pedido_compra and fk_pedido_venda:
                        model.create_funcionario(nome, fk_cliente, fk_pedido_compra, fk_pedido_venda)
                        st.success("Funcionário cadastrado com sucesso!")
                    else:
                        st.error("Preencha todos os campos!")
        
        with tab3:
            st.subheader("Editar/Excluir Funcionário")
            funcionarios = model.get_all_funcionarios()
            if funcionarios:
                funcionario_id = st.selectbox(
                    "Selecione o funcionário",
                    options=[f[0] for f in funcionarios],
                    format_func=lambda x: f"ID: {x}"
                )
                
                if funcionario_id:
                    funcionario = model.get_funcionario_by_id(funcionario_id)
                    if funcionario:
                        with st.form("editar_funcionario"):
                            nome = st.text_input("Nome", value=funcionario[1])
                            fk_cliente = st.number_input("ID do Cliente", value=funcionario[2])
                            fk_pedido_compra = st.number_input("ID do Pedido de Compra", value=funcionario[3])
                            fk_pedido_venda = st.number_input("ID do Pedido de Venda", value=funcionario[4])
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button("Atualizar"):
                                    model.update_funcionario(funcionario_id, nome, fk_cliente, fk_pedido_compra, fk_pedido_venda)
                                    st.success("Funcionário atualizado com sucesso!")
                            with col2:
                                if st.form_submit_button("Excluir"):
                                    model.delete_funcionario(funcionario_id)
                                    st.success("Funcionário excluído com sucesso!")
            else:
                st.info("Nenhum funcionário cadastrado.")
    
    def show_ingredientes(self, model):
        st.header("Gerenciamento de Ingredientes")
        
        tab1, tab2, tab3 = st.tabs(["Listar", "Adicionar", "Editar/Excluir"])
        
        with tab1:
            st.subheader("Lista de Ingredientes")
            ingredientes = model.get_all_ingredientes()
            if ingredientes:
                st.dataframe(ingredientes, column_config={
                    "id_ingredientes": "ID",
                    "quantidade": "Quantidade",
                    "validade": "Validade",
                    "desc": "Descrição",
                    "custo": "Custo",
                    "fk_produto": "Produto",
                    "fk_fornecedor": "Fornecedor"
                })
            else:
                st.info("Nenhum ingrediente cadastrado.")
        
        with tab2:
            st.subheader("Novo Ingrediente")
            with st.form("novo_ingrediente"):
                quantidade = st.number_input("Quantidade", min_value=1)
                validade = st.date_input("Validade")
                desc = st.text_input("Descrição")
                custo = st.number_input("Custo", min_value=0.0, step=0.01)
                fk_produto = st.number_input("ID do Produto", min_value=1)
                fk_fornecedor = st.number_input("ID do Fornecedor", min_value=1)
                
                if st.form_submit_button("Cadastrar"):
                    if quantidade and validade and desc and custo and fk_produto and fk_fornecedor:
                        model.create_ingrediente(quantidade, validade, desc, custo, fk_produto, fk_fornecedor)
                        st.success("Ingrediente cadastrado com sucesso!")
                    else:
                        st.error("Preencha todos os campos!")
        
        with tab3:
            st.subheader("Editar/Excluir Ingrediente")
            ingredientes = model.get_all_ingredientes()
            if ingredientes:
                ingrediente_id = st.selectbox(
                    "Selecione o ingrediente",
                    options=[i[0] for i in ingredientes],
                    format_func=lambda x: f"ID: {x}"
                )
                
                if ingrediente_id:
                    ingrediente = model.get_ingrediente_by_id(ingrediente_id)
                    if ingrediente:
                        with st.form("editar_ingrediente"):
                            quantidade = st.number_input("Quantidade", value=ingrediente[1])
                            validade = st.date_input("Validade", value=ingrediente[2])
                            desc = st.text_input("Descrição", value=ingrediente[3])
                            custo = st.number_input("Custo", value=ingrediente[4])
                            fk_produto = st.number_input("ID do Produto", value=ingrediente[5])
                            fk_fornecedor = st.number_input("ID do Fornecedor", value=ingrediente[6])
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button("Atualizar"):
                                    model.update_ingrediente(ingrediente_id, quantidade, validade, desc, custo, fk_produto, fk_fornecedor)
                                    st.success("Ingrediente atualizado com sucesso!")
                            with col2:
                                if st.form_submit_button("Excluir"):
                                    model.delete_ingrediente(ingrediente_id)
                                    st.success("Ingrediente excluído com sucesso!")
            else:
                st.info("Nenhum ingrediente cadastrado.")
    
    def show_produtos(self, model):
        st.header("Gerenciamento de Produtos")
        
        tab1, tab2, tab3 = st.tabs(["Listar", "Adicionar", "Editar/Excluir"])
        
        with tab1:
            st.subheader("Lista de Produtos")
            produtos = model.get_all_produtos()
            if produtos:
                st.dataframe(produtos, column_config={
                    "id_produto": "ID",
                    "desc": "Descrição",
                    "prec_venda": "Preço de Venda",
                    "fk_ingredientes": "Ingrediente",
                    "fk_pedido_venda": "Pedido Venda"
                })
            else:
                st.info("Nenhum produto cadastrado.")
        
        with tab2:
            st.subheader("Novo Produto")
            with st.form("novo_produto"):
                desc = st.text_input("Descrição")
                prec_venda = st.number_input("Preço de Venda", min_value=0.0, step=0.01)
                fk_ingredientes = st.number_input("ID do Ingrediente", min_value=1)
                fk_pedido_venda = st.number_input("ID do Pedido de Venda", min_value=1)
                
                if st.form_submit_button("Cadastrar"):
                    if desc and prec_venda and fk_ingredientes and fk_pedido_venda:
                        model.create_produto(desc, prec_venda, fk_ingredientes, fk_pedido_venda)
                        st.success("Produto cadastrado com sucesso!")
                    else:
                        st.error("Preencha todos os campos!")
        
        with tab3:
            st.subheader("Editar/Excluir Produto")
            produtos = model.get_all_produtos()
            if produtos:
                produto_id = st.selectbox(
                    "Selecione o produto",
                    options=[p[0] for p in produtos],
                    format_func=lambda x: f"ID: {x}"
                )
                
                if produto_id:
                    produto = model.get_produto_by_id(produto_id)
                    if produto:
                        with st.form("editar_produto"):
                            desc = st.text_input("Descrição", value=produto[1])
                            prec_venda = st.number_input("Preço de Venda", value=produto[2])
                            fk_ingredientes = st.number_input("ID do Ingrediente", value=produto[3])
                            fk_pedido_venda = st.number_input("ID do Pedido de Venda", value=produto[4])
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button("Atualizar"):
                                    model.update_produto(produto_id, desc, prec_venda, fk_ingredientes, fk_pedido_venda)
                                    st.success("Produto atualizado com sucesso!")
                            with col2:
                                if st.form_submit_button("Excluir"):
                                    model.delete_produto(produto_id)
                                    st.success("Produto excluído com sucesso!")
            else:
                st.info("Nenhum produto cadastrado.")
    
    def show_pedidos_compra(self, model):
        st.header("Gerenciamento de Pedidos de Compra")
        
        tab1, tab2, tab3 = st.tabs(["Listar", "Adicionar", "Editar/Excluir"])
        
        with tab1:
            st.subheader("Lista de Pedidos de Compra")
            pedidos = model.get_all_pedidos_compra()
            if pedidos:
                st.dataframe(pedidos, column_config={
                    "id_pedido": "ID",
                    "fk_fornecedor": "Fornecedor",
                    "fk_ingredientes": "Ingrediente"
                })
            else:
                st.info("Nenhum pedido de compra cadastrado.")
        
        with tab2:
            st.subheader("Novo Pedido de Compra")
            with st.form("novo_pedido_compra"):
                fk_fornecedor = st.number_input("ID do Fornecedor", min_value=1)
                fk_ingredientes = st.number_input("ID do Ingrediente", min_value=1)
                
                if st.form_submit_button("Cadastrar"):
                    if fk_fornecedor and fk_ingredientes:
                        model.create_pedido_compra(fk_fornecedor, fk_ingredientes)
                        st.success("Pedido de compra cadastrado com sucesso!")
                    else:
                        st.error("Preencha todos os campos!")
        
        with tab3:
            st.subheader("Editar/Excluir Pedido de Compra")
            pedidos = model.get_all_pedidos_compra()
            if pedidos:
                pedido_id = st.selectbox(
                    "Selecione o pedido",
                    options=[p[0] for p in pedidos],
                    format_func=lambda x: f"ID: {x}"
                )
                
                if pedido_id:
                    pedido = model.get_pedido_compra_by_id(pedido_id)
                    if pedido:
                        with st.form("editar_pedido_compra"):
                            fk_fornecedor = st.number_input("ID do Fornecedor", value=pedido[1])
                            fk_ingredientes = st.number_input("ID do Ingrediente", value=pedido[2])
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button("Atualizar"):
                                    model.update_pedido_compra(pedido_id, fk_fornecedor, fk_ingredientes)
                                    st.success("Pedido de compra atualizado com sucesso!")
                            with col2:
                                if st.form_submit_button("Excluir"):
                                    model.delete_pedido_compra(pedido_id)
                                    st.success("Pedido de compra excluído com sucesso!")
            else:
                st.info("Nenhum pedido de compra cadastrado.")
    
    def show_pedidos_venda(self, model):
        st.header("Gerenciamento de Pedidos de Venda")
        
        tab1, tab2, tab3 = st.tabs(["Listar", "Adicionar", "Editar/Excluir"])
        
        with tab1:
            st.subheader("Lista de Pedidos de Venda")
            pedidos = model.get_all_pedidos_venda()
            if pedidos:
                st.dataframe(pedidos, column_config={
                    "id_pedido_venda": "ID",
                    "fk_cliente": "Cliente",
                    "fk_funcionario": "Funcionário"
                })
            else:
                st.info("Nenhum pedido de venda cadastrado.")
        
        with tab2:
            st.subheader("Novo Pedido de Venda")
            with st.form("novo_pedido_venda"):
                fk_cliente = st.number_input("ID do Cliente", min_value=1)
                fk_funcionario = st.number_input("ID do Funcionário", min_value=1)
                
                if st.form_submit_button("Cadastrar"):
                    if fk_cliente and fk_funcionario:
                        model.create_pedido_venda(fk_cliente, fk_funcionario)
                        st.success("Pedido de venda cadastrado com sucesso!")
                    else:
                        st.error("Preencha todos os campos!")
        
        with tab3:
            st.subheader("Editar/Excluir Pedido de Venda")
            pedidos = model.get_all_pedidos_venda()
            if pedidos:
                pedido_id = st.selectbox(
                    "Selecione o pedido",
                    options=[p[0] for p in pedidos],
                    format_func=lambda x: f"ID: {x}"
                )
                
                if pedido_id:
                    pedido = model.get_pedido_venda_by_id(pedido_id)
                    if pedido:
                        with st.form("editar_pedido_venda"):
                            fk_cliente = st.number_input("ID do Cliente", value=pedido[1])
                            fk_funcionario = st.number_input("ID do Funcionário", value=pedido[2])
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button("Atualizar"):
                                    model.update_pedido_venda(pedido_id, fk_cliente, fk_funcionario)
                                    st.success("Pedido de venda atualizado com sucesso!")
                            with col2:
                                if st.form_submit_button("Excluir"):
                                    model.delete_pedido_venda(pedido_id)
                                    st.success("Pedido de venda excluído com sucesso!")
            else:
                st.info("Nenhum pedido de venda cadastrado.") 