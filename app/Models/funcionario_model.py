from typing import Optional
from datetime import date

class FuncionarioModel:
    def __init__(self, id_funcionario: Optional[int] = None, nome: str = "", 
                 dt_nascimento: Optional[date] = None, cpf: str = ""):
        self.id_funcionario = id_funcionario
        self.nome = nome
        self.dt_nascimento = dt_nascimento
        self.cpf = cpf
    
    def __repr__(self):
        return f"Funcionario(id={self.id_funcionario}, nome='{self.nome}', " \
               f"dt_nascimento={self.dt_nascimento}, cpf='{self.cpf}')"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id_funcionario': self.id_funcionario,
            'nome': self.nome,
            'dt_nascimento': self.dt_nascimento,
            'cpf': self.cpf
        } 