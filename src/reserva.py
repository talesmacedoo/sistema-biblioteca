from datetime import datetime

class Reserva:
    def __init__(self, usuario, livro):
        self.usuario = usuario
        self.livro = livro
        self.data_solicitacao = datetime.now()

#    def realizar_reserva(self):
#        return self.livro.realizar_reserva(self.usuario)

    def __str__(self):
        return f"Reserva para {self.livro.titulo} feita por {self.usuario.nome} em {self.data_solicitacao}"

