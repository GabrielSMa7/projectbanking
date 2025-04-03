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
            self.conta_poupanca = ContaPoupanca(saldo_inicial, self)
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

    def transferir(self, valor, destino_usuario):
        """Realiza transferência entre usuários"""
        if self.saldo < valor:
            print("Saldo insuficiente na conta corrente.")
            return
        
        senha_digitada = input("Digite sua senha para confirmar a transação: ")
        if senha_digitada != self.usuario.senha:
            print("Senha incorreta. Transação não realizada.")
            return

        self.saldo -= valor
        destino_usuario.conta_corrente.saldo += valor

        # Registra no histórico dos dois usuários
        self.historico.append(f"Transferência de R$ {valor:.2f} para {destino_usuario.nome} ({destino_usuario.cpf}).")
        destino_usuario.conta_corrente.historico.append(f"Recebido R$ {valor:.2f} de {self.usuario.nome} ({self.usuario.cpf}).")
        print("Transferência realizada com sucesso!")

    def transferir_para_poupanca(self, valor):
        """Transfere dinheiro da conta corrente para a poupança"""
        if self.saldo < valor:
            print("Saldo insuficiente na conta corrente.")
            return
        
        senha_digitada = input("Digite sua senha para confirmar a transação: ")
        if senha_digitada != self.usuario.senha:
            print("Senha incorreta. Transação não realizada.")
            return

        self.saldo -= valor
        self.usuario.conta_poupanca.saldo += valor

        # Registra no histórico
        self.historico.append(f"Transferência de R$ {valor:.2f} para a Conta Poupança.")
        self.usuario.conta_poupanca.historico.append(f"Recebido R$ {valor:.2f} da Conta Corrente.")
        print("Transferência realizada com sucesso!")

    def mostrar_historico(self):
        """Exibe o histórico de transações"""
        if not self.historico:
            print("Nenhuma transação realizada.")
        else:
            print("Histórico de Transações:")
            for transacao in self.historico:
                print(transacao)

class ContaPoupanca:
    def __init__(self, saldo=0, usuario=None):
        self.saldo = saldo
        self.historico = []
        self.usuario = usuario

    def transferir_para_corrente(self, valor):
        """Transfere dinheiro da conta poupança para a conta corrente"""
        if self.saldo < valor:
            print("Saldo insuficiente na conta poupança.")
            return
        
        senha_digitada = input("Digite sua senha para confirmar a transação: ")
        if senha_digitada != self.usuario.senha:
            print("Senha incorreta. Transação não realizada.")
            return

        self.saldo -= valor
        self.usuario.conta_corrente.saldo += valor

        # Registra no histórico
        self.historico.append(f"Transferência de R$ {valor:.2f} para a Conta Corrente.")
        self.usuario.conta_corrente.historico.append(f"Recebido R$ {valor:.2f} da Conta Poupança.")
        print("Transferência realizada com sucesso!")

    def mostrar_historico(self):
        """Exibe o histórico de transações"""
        if not self.historico:
            print("Nenhuma transação realizada.")
        else:
            print("Histórico de Transações:")
            for transacao in self.historico:
                print(transacao)

usuarios = {}

def menu():
    while True:
        print("\n1. Criar Usuário")
        print("2. Criar Conta Corrente")
        print("3. Criar Conta Poupança")
        print("4. Ver Saldo")
        print("5. Transferir entre Usuários")
        print("6. Transferir entre Minhas Contas")
        print("7. Ver Histórico de Transações")
        print("8. Sair")
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
            cpf_origem = input("Digite o CPF do remetente: ")
            if cpf_origem in usuarios:
                cpf_destino = input("Digite o CPF do destinatário: ")
                if cpf_destino in usuarios and cpf_origem != cpf_destino:
                    valor = float(input("Digite o valor da transferência: "))
                    usuarios[cpf_origem].conta_corrente.transferir(valor, usuarios[cpf_destino])
                else:
                    print("Usuário de destino inválido ou é o mesmo que o de origem.")
            else:
                print("Usuário de origem não encontrado.")

        elif opcao == "6":
            cpf = input("Digite seu CPF: ")
            if cpf in usuarios:
                usuario = usuarios[cpf]
                if usuario.conta_corrente and usuario.conta_poupanca:
                    print("\n1. Transferir da Corrente para a Poupança")
                    print("2. Transferir da Poupança para a Corrente")
                    escolha = input("Escolha a opção: ")

                    valor = float(input("Digite o valor da transferência: "))

                    if escolha == "1":
                        usuario.conta_corrente.transferir_para_poupanca(valor)
                    elif escolha == "2":
                        usuario.conta_poupanca.transferir_para_corrente(valor)
                    else:
                        print("Opção inválida.")
                else:
                    print("Usuário não tem ambas as contas.")
            else:
                print("Usuário não encontrado.")

        elif opcao == "7":
            cpf = input("Digite o CPF para ver o histórico: ")
            if cpf in usuarios:
                usuarios[cpf].conta_corrente.mostrar_historico()
            else:
                print("Usuário não encontrado.")

        elif opcao == "8":
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

menu()
