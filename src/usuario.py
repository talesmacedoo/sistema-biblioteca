from datetime import datetime


class Usuario:
    def __init__(self, codigo, nome, tipo):
        self.codigo = codigo
        self.nome = nome
        self.tipo = tipo
        self.emprestimos = []
        self.reservas = []

    def realizar_reserva(self, livro):
        if livro.realizar_reserva(self):
            self.reservas.append(livro)
            return True
        return False

    def possui_reserva(self, livro):
        return livro in self.reservas

    def consultar_emprestimos(self):
        return [{"Livro": livro.titulo, "Data Empréstimo": exemplar.data_emprestimo, "Status": "Empréstimo Ativo"
                 if exemplar.data_prevista_devolucao > datetime.now() else "Empréstimo Finalizado"} for livro, exemplar in self.emprestimos]

    def consultar_reservas(self):
        return [livro.titulo for livro in self.reservas]

    

class AlunoGraduacao(Usuario):
    def __init__(self, codigo, nome):
        super().__init__(codigo, nome, "Aluno de Graduação")
        self.tempo_emprestimo = 3  

class AlunoPos(Usuario):
    def __init__(self, codigo, nome):
        super().__init__(codigo, nome, "Aluno de Pós-Graduação")
        self.tempo_emprestimo = 4  


class Professor(Usuario):
    def __init__(self, codigo, nome):
        super().__init__(codigo, nome, "Professor")
        self.tempo_emprestimo = 7  
        self.observacoes = 0

    def observar_livro(self, livro):
        livro.adicionar_observador(self)

    def notificado_sobre_reservas(self):
        self.observacoes += 1
        print(f"{self.nome} foi notificado sobre mais de duas reservas simultâneas.")

class Observador(Professor, Usuario):
    def __init__(self, codigo, nome):
        super().__init__(codigo, nome)


