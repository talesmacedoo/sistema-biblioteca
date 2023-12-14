from command import Command

class RealizarDevolucao(Command):
    def __init__(self, sistema, codigo_usuario, codigo_livro):
        self.sistema = sistema
        self.codigo_usuario = codigo_usuario
        self.codigo_livro = codigo_livro

    def execute(self):
        return self.sistema.realizar_devolucao(self.codigo_usuario, self.codigo_livro)
