-- Create clientes table
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    mesa INTEGER NOT NULL,
    cpf TEXT UNIQUE NOT NULL
);

-- Create funcionarios table
CREATE TABLE IF NOT EXISTS funcionarios (
    id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    dt_nascimento DATE NOT NULL,
    cpf TEXT UNIQUE NOT NULL
);

-- Create fornecedores table
CREATE TABLE IF NOT EXISTS fornecedores (
    id_fornecedor INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cnpj TEXT UNIQUE NOT NULL
);

-- Create ingredientes table
CREATE TABLE IF NOT EXISTS ingredientes (
    id_ingrediente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_i TEXT NOT NULL,
    valor_compra REAL NOT NULL,
    quantidade REAL NOT NULL,
    fk_fornecedor INTEGER NOT NULL,
    FOREIGN KEY (fk_fornecedor) REFERENCES fornecedores(id_fornecedor)
);

-- Create produtos table
CREATE TABLE IF NOT EXISTS produtos (
    id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_p TEXT NOT NULL,
    quantidade INTEGER NOT NULL DEFAULT 0,
    descricao TEXT,
    valor_venda REAL NOT NULL
);

-- Create produto_ingredientes table
CREATE TABLE IF NOT EXISTS produto_ingredientes (
    fk_produto INTEGER NOT NULL,
    fk_ingrediente INTEGER NOT NULL,
    quantidade_necessaria REAL NOT NULL,
    PRIMARY KEY (fk_produto, fk_ingrediente),
    FOREIGN KEY (fk_produto) REFERENCES produtos(id_produto),
    FOREIGN KEY (fk_ingrediente) REFERENCES ingredientes(id_ingrediente)
);

-- Create pedido_venda table
CREATE TABLE IF NOT EXISTS pedido_venda (
    id_pedido_venda INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_cliente INTEGER NOT NULL,
    fk_produto INTEGER NOT NULL,
    qtd_venda INTEGER NOT NULL,
    data_venda DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (fk_produto) REFERENCES produtos(id_produto)
);

-- Create pedido_compra table
CREATE TABLE IF NOT EXISTS pedido_compra (
    id_pedido_compra INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_funcionario INTEGER NOT NULL,
    fk_ingrediente INTEGER NOT NULL,
    qtd_ingrediente REAL NOT NULL,
    data_compra DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_funcionario) REFERENCES funcionarios(id_funcionario),
    FOREIGN KEY (fk_ingrediente) REFERENCES ingredientes(id_ingrediente)
); 