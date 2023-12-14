from command import Command

class RealizarEmprestimo(Command):
    def __init__(self, sistema, codigo_usuario, codigo_livro):
        self.sistema = sistema
        self.codigo_usuario = codigo_usuario
        self.codigo_livro = codigo_livro

    def execute(self):
        return self.sistema.realizar_emprestimo(self.codigo_usuario, self.codigo_livro)
