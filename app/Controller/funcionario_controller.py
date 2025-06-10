from typing import List, Optional, Tuple
from Models.funcionario_model import FuncionarioModel
from Repository.funcionario_repo import FuncionarioRepository
from datetime import date

from Validations.cpf import validate_cpf

class FuncionarioController:
    def __init__(self):
        self.repository = FuncionarioRepository()
    
    def create_funcionario(self, nome: str, dt_nascimento: date, cpf: str) -> Tuple[bool, str]:
        # Validate CPF format
        if not validate_cpf(cpf):
            return False, "CPF inválido"
        
        # Check if CPF already exists
        if self.repository.get_funcionario_by_cpf(cpf):
            return False, "CPF já cadastrado"
        
        # Create and save funcionario
        funcionario = FuncionarioModel(nome=nome, dt_nascimento=dt_nascimento, cpf=cpf)
        self.repository.add_funcionario(funcionario)
        return True, "Funcionário cadastrado com sucesso"
    
    def list_funcionarios(self) -> List[FuncionarioModel]:
        return self.repository.get_all_funcionarios()
    
    def get_funcionario(self, id_funcionario: int) -> Optional[FuncionarioModel]:
        return self.repository.get_funcionario_by_id(id_funcionario)
    
    def update_funcionario_info(self, id_funcionario: int, nome: str, dt_nascimento: date) -> Tuple[bool, str]:
        funcionario = self.repository.get_funcionario_by_id(id_funcionario)
        if not funcionario:
            return False, "Funcionário não encontrado"
        
        funcionario.nome = nome
        funcionario.dt_nascimento = dt_nascimento
        self.repository.update_funcionario(id_funcionario, funcionario)
        return True, "Funcionário atualizado com sucesso"
    
    def remove_funcionario(self, id_funcionario: int) -> Tuple[bool, str]:
        funcionario = self.repository.get_funcionario_by_id(id_funcionario)
        if not funcionario:
            return False, "Funcionário não encontrado"
        
        self.repository.delete_funcionario(id_funcionario)
        return True, "Funcionário removido com sucesso" 