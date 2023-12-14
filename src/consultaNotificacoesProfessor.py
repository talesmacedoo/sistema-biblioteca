from command import Command

class ConsultaNotificacoesProfessor(Command):
    def __init__(self, sistema, codigo_usuario):
        self.sistema = sistema
        self.codigo_usuario = codigo_usuario

    def execute(self):
        return self.sistema.consultar_notificacoes_professor(self.codigo_usuario)