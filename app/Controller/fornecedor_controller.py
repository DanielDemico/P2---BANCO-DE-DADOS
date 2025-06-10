from typing import List, Optional, Tuple
from Models.fornecedor_model import FornecedorModel
from Repository.fornecedor_repo import FornecedorRepository

from Validations.cnpj import validate_cnpj

class FornecedorController:
    def __init__(self):
        self.repository = FornecedorRepository()
    
    def create_fornecedor(self, nome: str, cnpj: str) -> Tuple[bool, str]:
        # Validate CNPJ format
        if not validate_cnpj(cnpj):
            return False, "CNPJ inválido"
        
        # Check if CNPJ already exists
        if self.repository.get_fornecedor_by_cnpj(cnpj):
            return False, "CNPJ já cadastrado"
        
        # Create and save fornecedor
        fornecedor = FornecedorModel(nome=nome, cnpj=cnpj)
        self.repository.add_fornecedor(fornecedor)
        return True, "Fornecedor cadastrado com sucesso"
    
    def list_fornecedores(self) -> List[FornecedorModel]:
        return self.repository.get_all_fornecedores()
    
    def get_fornecedor(self, id_fornecedor: int) -> Optional[FornecedorModel]:
        return self.repository.get_fornecedor_by_id(id_fornecedor)
    
    def get_fornecedor_para_display(self) -> List[Tuple[int, str]]:
        """Returns list of (id, nome) tuples for selectboxes"""
        fornecedores = self.list_fornecedores()
        return [(f.id_fornecedor, f.nome) for f in fornecedores]
    
    def update_fornecedor_info(self, id_fornecedor: int, nome: str) -> Tuple[bool, str]:
        fornecedor = self.repository.get_fornecedor_by_id(id_fornecedor)
        if not fornecedor:
            return False, "Fornecedor não encontrado"
        
        fornecedor.nome = nome
        self.repository.update_fornecedor(id_fornecedor, fornecedor)
        return True, "Fornecedor atualizado com sucesso"
    
    def remove_fornecedor(self, id_fornecedor: int) -> Tuple[bool, str]:
        fornecedor = self.repository.get_fornecedor_by_id(id_fornecedor)
        if not fornecedor:
            return False, "Fornecedor não encontrado"
        
        # Check for dependencies
        if self.repository.check_dependencies(id_fornecedor):
            return False, "Não é possível deletar o fornecedor pois existem ingredientes vinculados a ele"
        
        self.repository.delete_fornecedor(id_fornecedor)
        return True, "Fornecedor removido com sucesso" 