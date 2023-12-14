from command import Command

class Sair(Command):
    def __init__(self, sistema):
        self.sistema = sistema

    def execute(self):
        self.sistema.sair()
        return (True, "Saindo....")