import sqlite3
import os

def get_db_path():
    """Get the path to the database file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "villa.db")

def get_connection():
    """Get a connection to the database"""
    return sqlite3.connect(get_db_path())

def init_db():
    """Initialize the database by creating all tables"""
    # Import all repositories to ensure their schemas are registered
    from Repository.cliente_repo import ClienteRepository
    from Repository.funcionario_repo import FuncionarioRepository
    from Repository.fornecedor_repo import FornecedorRepository
    from Repository.ingrediente_repo import IngredienteRepository
    from Repository.produto_repo import ProdutoRepository
    from Repository.produto_ingredientes_repo import ProdutoIngredientesRepository
    from Repository.pedido_venda_repo import PedidoVendaRepository
    from Repository.pedido_compra_repo import PedidoCompraRepository

    # Create tables by initializing repositories
    ClienteRepository().create_table()
    FuncionarioRepository().create_table()
    FornecedorRepository().create_table()
    IngredienteRepository().create_table()
    ProdutoRepository().create_table()
    ProdutoIngredientesRepository().create_table()
    PedidoVendaRepository().create_table()
    PedidoCompraRepository().create_table()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!") 