from typing import List, Optional, Tuple
from Models.cliente_model import ClienteModel
from Repository.cliente_repo import ClienteRepository

from Validations.cpf import validate_cpf

class ClienteController:
    def __init__(self):
        self.repository = ClienteRepository()
    
    def create_cliente(self, nome: str, mesa: int, cpf: str) -> Tuple[bool, str]:
        # Validate CPF format
        if not validate_cpf(cpf):
            return False, "CPF inválido"
        
        # Check if CPF already exists
        if self.repository.get_cliente_by_cpf(cpf):
            return False, "CPF já cadastrado"
        
        # Create and save cliente
        cliente = ClienteModel(nome=nome, mesa=mesa, cpf=cpf)
        self.repository.add_cliente(cliente)
        return True, "Cliente cadastrado com sucesso"
    
    def list_clientes(self) -> List[ClienteModel]:
        return self.repository.get_all_clientes()
    
    def get_cliente(self, id_cliente: int) -> Optional[ClienteModel]:
        return self.repository.get_cliente_by_id(id_cliente)
    
    def update_cliente_info(self, id_cliente: int, nome: str, mesa: int) -> Tuple[bool, str]:
        cliente = self.repository.get_cliente_by_id(id_cliente)
        if not cliente:
            return False, "Cliente não encontrado"
        
        cliente.nome = nome
        cliente.mesa = mesa
        self.repository.update_cliente(id_cliente, cliente)
        return True, "Cliente atualizado com sucesso"
    
    def remove_cliente(self, id_cliente: int) -> Tuple[bool, str]:
        cliente = self.repository.get_cliente_by_id(id_cliente)
        if not cliente:
            return False, "Cliente não encontrado"
        
        self.repository.delete_cliente(id_cliente)
        return True, "Cliente removido com sucesso"
    
    def search_clientes(self, query: str, search_by: str) -> List[ClienteModel]:
        if search_by == "nome":
            return self.repository.search_clientes_by_nome(query)
        elif search_by == "cpf":
            cliente = self.repository.get_cliente_by_cpf(query)
            return [cliente] if cliente else []
        return [] 