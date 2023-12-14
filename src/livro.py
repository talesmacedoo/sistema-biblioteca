from datetime import datetime, timedelta
from exemplar import Exemplar
from usuario import AlunoGraduacao, AlunoPos, Professor
from reserva import Reserva
from emprestimo import Emprestimo

class Livro:
    def __init__(self, codigo, titulo, editora, autores, edicao, ano_publicacao):
        self.codigo = codigo
        self.titulo = titulo
        self.editora = editora
        self.autores = autores
        self.edicao = edicao
        self.ano_publicacao = ano_publicacao
        self.exemplares = []  
        self.reservas = []
        self.emprestimos = []
        self.observadores = set()

    def adicionar_exemplar(self, codigo_exemplar):
        exemplar = Exemplar(codigo_exemplar, self)
        self.exemplares.append(exemplar)

    def realizar_emprestimo(self, usuario):
        exemplares_disponiveis = self.exemplares_disponiveis()
        if len(exemplares_disponiveis) == 0:
            return False, "Não há exemplares disponíveis para empréstimo."

        #if usuario.devedor():
        #    return False, "Usuário está com débitos pendentes. Empréstimo não permitido."

        # Verifica as regras para alunos e professores
        if isinstance(usuario, AlunoGraduacao) and len(usuario.emprestimos) >= 3:
            return False, "Limite de empréstimos para Aluno de Graduação atingido."

        elif isinstance(usuario, AlunoPos) and len(usuario.emprestimos) >= 4:
            return False, "Limite de empréstimos para Aluno de Pós-Graduação atingido."
        if len(self.reservas) >= len(exemplares_disponiveis):
            reservas_do_usuario = [reserva.livro for reserva in self.reservas if reserva.usuario == usuario]
            if not reservas_do_usuario or self not in reservas_do_usuario:
                return False, "Não é possível realizar o empréstimo. Já existem reservas para todos os exemplares"

        #Checando se tem algum empréstimo em curso do mesmo livro
        if any(emprestimo.livro == self and emprestimo.status == "Em curso" for emprestimo in usuario.emprestimos):
            return False, "Usuário já possui empréstimo em curso deste livro."

        #Todas as condições atendidas
        emprestimo = Emprestimo(usuario, self, self.exemplares_disponiveis()[0])
        self.emprestimos.append(emprestimo)
        usuario.emprestimos.append(emprestimo)
        self.exemplares_disponiveis()[0].status = "Emprestado"
        emprestimo.data_devolucao_prevista = datetime.now() + timedelta(days=usuario.tempo_emprestimo)
        return True, "Empréstimo realizado com sucesso."
    
    def exemplares_disponiveis(self):
        exemplares_disponiveis = [exemplar for exemplar in self.exemplares if exemplar.status == "Disponível"]
        return exemplares_disponiveis


    def realizar_devolucao(self, usuario):
        for exemplar in self.exemplares:
            if exemplar.usuario_emprestado == usuario:
                devolucao_sucesso = exemplar.devolver()
                if devolucao_sucesso:
                    
                    return True
        return False

    def realizar_reserva(self, usuario):
        reserva = Reserva(usuario, self)
        self.reservas.append(reserva)

        
        self.notificar_observadores()

        return True  

    def adicionar_observador(self, usuario):
        self.observadores.add(usuario)

    def notificar_observadores(self):
        if len(self.reservas) > 2:
            for observador in self.observadores:
                observador.notificado_sobre_reservas()

    def consultar_status(self):
        
        status_exemplares = [exemplar.consultar_status() for exemplar in self.exemplares]
        return {
            "titulo": self.titulo,
            "codigo": self.codigo,
            "status_exemplares": status_exemplares,
            "reservas": [usuario.nome for usuario in self.reservas],
        }

