def menu():
    menu = """ =============== MENU ================
[d]\tDepositar
[s]\tSacar
[e]\tExtrato
[nc]\tNova conta
[lc]\tListar contas
[nu]\tNovo usuário
[q]\tSair
=> """
    return input(menu)

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("=== Deposito realizado com sucesso! ===")
        
    else:
        print("@@@ Operação falhou! O valor informado é inválido!")
    
    return saldo, extrato

def sacar(saldo, valor, extrato, limite, numero_saques, limites_saques):
    if valor > saldo:
        print("@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    elif valor > limite:
        print("@@@ Operação falhou! O valor do saque excede o limite. @@@")

    elif  numero_saques >= limites_saques:
        print("@@@ Operação falhou! Número máximo de saques excedido. @@@")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    print("=========================================")

def criar_usuarios(usuarios):
    cpf = input("Informe o CPF (somente números): ").strip()
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        print("@@@ Já existe um usuário com esse CPF! @@@")
        return
    
    nome = input("Informe o nome completo: ").strip()
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa)").strip()
    endereco = input("Informe o endereço (longadouro, nº - bairro - cidade/estado): ").strip()

    usuarios.append({
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "endereco": endereco
    })

    print("=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf, usuarios):
    for usuario in usuarios:

        if usuario["cpf"] == cpf:
            return usuario
        
    return None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ").strip()
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("=== Conta criada com sucesso! ===")
        return {
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario
        }

    print("@@@ Usuário não encontrado, criação de conta cancelada. @@@")
    return None

def listar_contas(contas):
    if not contas:
        print("=== Nenhuma conta cadastrada. ===")
        return
    
    for conta in contas:
        linha = f"""\
            Agência: {conta['agencia']}
            Conta: {conta['numero_conta']}
            Titular: {conta['usuario']['nome']}
        """
        print("=" * 30)
        print(linha)
    
def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    numero_conta = 1
    usuarios = []
    contas = []
    


    while True:
        opcao = menu().lower()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: R$"))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: R$"))
            saldo, extrato, numero_saques = sacar(
                saldo = saldo, 
                valor = valor,
                extrato = extrato, 
                limite = limite, 
                numero_saques = numero_saques, 
                limites_saques = LIMITE_SAQUES
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato = extrato)

        elif opcao == 'nc':
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
                numero_conta += 1

        elif opcao == 'lc':
            listar_contas(contas)

        elif opcao == 'nu':
            criar_usuarios(usuarios)

        elif opcao == "q":
            print("\n=== Obrigado por utilizar nosso sistema! Até logo. ===")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
        
main()
