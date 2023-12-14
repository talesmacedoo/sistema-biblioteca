from command import Command

class ConsultaUsuario(Command):
    def __init__(self, sistema, codigo_usuario):
        self.sistema = sistema
        self.codigo_usuario = codigo_usuario

    def execute(self):
        return self.sistema.consultar_usuario(self.codigo_usuario)