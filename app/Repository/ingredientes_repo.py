import sqlite3

class IngredienteRepository:
    def __init__(self):
        self.connection = sqlite3.connect('villa.db')
        self.cursor = self.connection.cursor()
        
        # Cria a tabela se não existir
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ingredientes (
                id_ingredientes INTEGER PRIMARY KEY AUTOINCREMENT,
                quantidade INTEGER NOT NULL,
                validade DATE,
                desc VARCHAR(255) NOT NULL,
                custo REAL NOT NULL,
                fk_produto INTEGER NOT NULL,
                fk_fornecedor INTEGER NOT NULL,
                FOREIGN KEY (fk_produto) REFERENCES produtos(id_produto),
                FOREIGN KEY (fk_fornecedor) REFERENCES fornecedor(id_fornecedor)
            );
        """)
        self.connection.commit()
    
    def get_all(self):
        self.cursor.execute("SELECT * FROM ingredientes")
        return self.cursor.fetchall()
    
    def get_by_id(self, id):
        self.cursor.execute("SELECT * FROM ingredientes WHERE id_ingredientes = ?", (id,))
        return self.cursor.fetchone()
    
    def create(self, quantidade, validade, desc, custo, fk_produto, fk_fornecedor):
        self.cursor.execute("""
            INSERT INTO ingredientes (quantidade, validade, desc, custo, fk_produto, fk_fornecedor)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (quantidade, validade, desc, custo, fk_produto, fk_fornecedor))
        self.connection.commit()
        return self.cursor.lastrowid
    
    def update(self, id, quantidade, validade, desc, custo, fk_produto, fk_fornecedor):
        self.cursor.execute("""
            UPDATE ingredientes 
            SET quantidade = ?, validade = ?, desc = ?, custo = ?, fk_produto = ?, fk_fornecedor = ?
            WHERE id_ingredientes = ?
        """, (quantidade, validade, desc, custo, fk_produto, fk_fornecedor, id))
        self.connection.commit()
        return True
    
    def delete(self, id):
        self.cursor.execute("DELETE FROM ingredientes WHERE id_ingredientes = ?", (id,))
        self.connection.commit()
        return True
    
    def __del__(self):
        self.connection.close()