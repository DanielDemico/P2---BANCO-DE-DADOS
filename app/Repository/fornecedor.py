import sqlite3

class FornecedorRepository:
    def __init__(self):
        self.connection = sqlite3.connect('villa.db')
        self.cursor = self.connection.cursor()
        
        # Cria a tabela se não existir
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS fornecedores(
                id_fornecedores INTEGER PRIMARY KEY AUTOINCREMENT,
                CNPJ VARCHAR(26) NOT NULL,
                fk_pedido_compra INTEGER NOT NULL,
                fk_ingredientes INTEGER NOT NULL,
                FOREIGN KEY (fk_pedido_compra) REFERENCES pedidos(id_pedido),
                FOREIGN KEY (fk_ingredientes) REFERENCES ingrediente(id_ingredientes)
            );
        """)
        self.connection.commit()
    
    def get_all(self):
        self.cursor.execute("SELECT * FROM fornecedores")
        return self.cursor.fetchall()
    
    def get_by_id(self, id):
        self.cursor.execute("SELECT * FROM fornecedores WHERE id_fornecedores = ?", (id,))
        return self.cursor.fetchone()
    
    def create(self, cnpj, fk_pedido_compra, fk_ingredientes):
        self.cursor.execute("""
            INSERT INTO fornecedores (CNPJ, fk_pedido_compra, fk_ingredientes)
            VALUES (?, ?, ?)
        """, (cnpj, fk_pedido_compra, fk_ingredientes))
        self.connection.commit()
        return self.cursor.lastrowid
    
    def update(self, id, cnpj, fk_pedido_compra, fk_ingredientes):
        self.cursor.execute("""
            UPDATE fornecedores 
            SET CNPJ = ?, fk_pedido_compra = ?, fk_ingredientes = ?
            WHERE id_fornecedores = ?
        """, (cnpj, fk_pedido_compra, fk_ingredientes, id))
        self.connection.commit()
        return True
    
    def delete(self, id):
        self.cursor.execute("DELETE FROM fornecedores WHERE id_fornecedores = ?", (id,))
        self.connection.commit()
        return True
    
    def __del__(self):
        self.connection.close()