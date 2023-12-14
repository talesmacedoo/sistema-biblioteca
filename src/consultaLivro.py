from command import Command

class ConsultaLivro(Command):
    def __init__(self, sistema, codigo_livro):
        self.sistema = sistema
        self.codigo_livro = codigo_livro

    def execute(self):
        return self.sistema.consultar_livro(self.codigo_livro)
