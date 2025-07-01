from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
        
        if valor > self._saldo:
            print("\n@@@ Operação falhou! Saldo insuficiente. @@@")
            return False
        
        self._saldo -= valor
        print("\n=== Saque realizado com sucesso! ===")
        return True
    
    def depositar(self, valor):
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
        
        self._saldo += valor
        print("\n=== Depósito realizado com sucesso! ===")
        return True

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
        )

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [t for t in self.historico.transacoes if t["tipo"] == Saque.__name__]
        )

        if valor > self._limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
            return False

        if numero_saques >= self._limite_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
            return False
        
        return super().sacar(valor)

    def __str__(self):
        return f"""
Agência:\t{self.agencia}
Conta:\t\t{self.numero}
Titular:\t{self.cliente.nome}
"""

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def executar(self, conta):
        pass

    def registrar(self, conta):
        sucesso = self.executar(conta)
        if sucesso:
            conta.historico.adicionar(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def executar(self, conta):
        return conta.depositar(self._valor)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def executar(self, conta):
        return conta.sacar(self._valor)
    
def menu():
    menu_texto = """
=============== MENU ===============
[d]\tDepositar
[s]\tSacar
[e]\tExtrato
[nc]\tNova conta
[lc]\tListar contas
[nu]\tNovo usuário
[q]\tSair
=> """
    return input(menu_texto)

def filtrar_cliente(cpf, clientes):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente números): ").strip()
    cliente = filtrar_cliente(cpf, clientes)
    
    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return
    
    nome = input("Informe o nome completo: ").strip()
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ").strip()
    endereco = input("Informe o endereço (logradouro, nº - bairro - cidade/estado): ").strip()
    
    novo_cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
    clientes.append(novo_cliente)
    print("\n=== Cliente criado com sucesso! ===")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    print("\n=== Conta criada com sucesso! ===")

def listar_contas(contas):
    if not contas:
        print("\n@@@ Ainda não existem contas cadastradas! @@@")
        return

    for conta in contas:
        print("="*30)
        print(conta)
        print("="*30)

def extrato(conta):
    print("\n====== EXTRATO ======")
    if not conta.historico.transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in conta.historico.transacoes:
            print(f"{transacao['data']} - {transacao['tipo']}: R$ {transacao['valor']:.2f}")
    print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
    print("=====================\n")

def main():
    clientes = []
    contas = []
    numero_conta = 1

    while True:
        opcao = menu()

        if opcao == 'd':
            cpf = input("Informe o CPF do cliente: ").strip()
            cliente = filtrar_cliente(cpf, clientes)
            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue
            
            if not cliente.contas:
                print("\n@@@ Cliente não possui contas! @@@")
                continue
            
            conta = cliente.contas[0]
            valor = float(input("Informe o valor do depósito: "))
            deposito = Deposito(valor)
            cliente.realizar_transacao(conta, deposito)

        elif opcao == 's':
            cpf = input("Informe o CPF do cliente: ").strip()
            cliente = filtrar_cliente(cpf, clientes)
            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue

            if not cliente.contas:
                print("\n@@@ Cliente não possui contas! @@@")
                continue

            conta = cliente.contas[0]
            valor = float(input("Informe o valor do saque: "))
            saque = Saque(valor)
            cliente.realizar_transacao(conta, saque)

        elif opcao == 'e':
            cpf = input("Informe o CPF do cliente: ").strip()
            cliente = filtrar_cliente(cpf, clientes)
            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue

            if not cliente.contas:
                print("\n@@@ Cliente não possui contas! @@@")
                continue

            conta = cliente.contas[0]
            extrato(conta)

        elif opcao == 'nc':
            criar_conta(numero_conta, clientes, contas)
            numero_conta += 1

        elif opcao == 'lc':
            listar_contas(contas)

        elif opcao == 'nu':
            criar_cliente(clientes)

        elif opcao == 'q':
            print("Encerrando o sistema... Até mais!")
            break

        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()