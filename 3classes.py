class Usuario:
    def __init__(self, nome, cpf, senha):
        self.nome = nome
        self.cpf = cpf
        self.senha = senha
        self.conta_corrente = None
        self.conta_poupanca = None

    def criar_conta_corrente(self, saldo_inicial):
        if self.conta_corrente is None:
            self.conta_corrente = ContaCorrente(saldo_inicial, self)
            print(f"Conta Corrente criada com saldo de R$ {saldo_inicial:.2f}")
        else:
            print("Usuário já possui uma conta corrente.")

    def criar_conta_poupanca(self, saldo_inicial):
        if self.conta_poupanca is None:
            self.conta_poupanca = ContaPoupanca(saldo_inicial)
            print(f"Conta Poupança criada com saldo de R$ {saldo_inicial:.2f}")
        else:
            print("Usuário já possui uma conta poupança.")

    def mostrar_saldo(self):
        saldo_cc = self.conta_corrente.saldo if self.conta_corrente else 0
        saldo_cp = self.conta_poupanca.saldo if self.conta_poupanca else 0
        print(f"Saldo Conta Corrente: R$ {saldo_cc:.2f}")
        print(f"Saldo Conta Poupança: R$ {saldo_cp:.2f}")
        print(f"Total de Patrimônio: R$ {saldo_cp + saldo_cc:.2f}")

class ContaCorrente:
    def __init__(self, saldo=0, usuario=None):
        self.saldo = saldo
        self.historico = []  # Histórico de transações
        self.usuario = usuario  # Referência ao usuário

    def realizar_transacao(self, valor, tipo, destino_usuario=None):
        """Realiza a transação e registra no histórico."""
        if self.saldo < valor:
            print("Saldo insuficiente para a transferência.")
            return
        
        senha_digitada = input("Digite a sua senha para confirmar a transação: ")
        if senha_digitada != self.usuario.senha:
            print("Senha incorreta. Transação não realizada.")
            return
        
        if tipo == 'transferencia':
            self.saldo -= valor
            destino_usuario.conta_corrente.saldo += valor
            # Adiciona no histórico dos dois usuários
            self.historico.append(f"Transferência de R$ {valor:.2f} para {destino_usuario.nome} ({destino_usuario.cpf}).")
            destino_usuario.conta_corrente.historico.append(f"Recebido R$ {valor:.2f} de {self.usuario.nome} ({self.usuario.cpf}).")
            print(f"Transferência realizada com sucesso!")
        else:
            print("Tipo de transação inválido.")
            
    def mostrar_historico(self):
        """Exibe o histórico de transações da conta corrente."""
        if not self.historico:
            print("Nenhuma transação realizada.")
        else:
            print("Histórico de Transações:")
            for transacao in self.historico:
                print(transacao)

class ContaPoupanca:
    def __init__(self, saldo=0):
        self.saldo = saldo

usuarios = {}

def menu():
    while True:
        print("\n1. Criar Usuário")
        print("2. Criar Conta Corrente")
        print("3. Criar Conta Poupança")
        print("4. Ver Saldo")
        print("5. Realizar Transferência")
        print("6. Ver Histórico de Transações")
        print("7. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            cpf = input("CPF: ")
            senha = input("Senha: ")
            if cpf not in usuarios:
                usuarios[cpf] = Usuario(nome, cpf, senha)
                print("Usuário criado com sucesso!")
            else:
                print("Já existe um usuário com esse CPF.")

        elif opcao == "2":
            cpf = input("Digite o CPF: ")
            if cpf in usuarios:
                saldo_inicial = float(input("Saldo inicial: "))
                usuarios[cpf].criar_conta_corrente(saldo_inicial)
            else:
                print("Usuário não encontrado.")

        elif opcao == "3":
            cpf = input("Digite o CPF: ")
            if cpf in usuarios:
                saldo_inicial = float(input("Saldo inicial: "))
                usuarios[cpf].criar_conta_poupanca(saldo_inicial)
            else:
                print("Usuário não encontrado.")

        elif opcao == "4":
            cpf = input("Digite o CPF: ")
            if cpf in usuarios:
                usuarios[cpf].mostrar_saldo()
            else:
                print("Usuário não encontrado.")

        elif opcao == "5":
            cpf_origem = input("Digite o CPF do usuário de origem: ")
            if cpf_origem in usuarios:
                cpf_destino = input("Digite o CPF do usuário de destino: ")
                if cpf_destino in usuarios and cpf_origem != cpf_destino:
                    valor = float(input("Digite o valor da transferência: "))
                    usuarios[cpf_origem].conta_corrente.realizar_transacao(valor, 'transferencia', usuarios[cpf_destino])
                else:
                    print("Usuário de destino inválido ou é o mesmo que o de origem.")
            else:
                print("Usuário de origem não encontrado.")
                
        elif opcao == "6":
            cpf = input("Digite o CPF para ver o histórico: ")
            if cpf in usuarios:
                usuarios[cpf].conta_corrente.mostrar_historico()
            else:
                print("Usuário não encontrado.")

        elif opcao == "7":
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

menu()
