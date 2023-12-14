from datetime import datetime, timedelta


class Exemplar:
    def __init__(self, codigo, livro):
        self.codigo = codigo
        self.livro = livro
        self.status = "Disponível"  #  "Disponível" | "Emprestado"
        self.usuario_emprestado = None
        self.data_emprestimo = None
        self.data_devolucao_prevista = None

    def emprestar(self, usuario):
        if self.status == "Disponível":
            self.status = "Emprestado"
            self.usuario_emprestado = usuario
            self.data_emprestimo = datetime.now()
            prazo_emprestimo = usuario.tempo_emprestimo 
            self.data_devolucao_prevista = self.data_emprestimo + timedelta(days=prazo_emprestimo)
            return True
        else:
            return False

    def devolver(self):
        if self.status == "Emprestado":
            self.status = "Disponível"
            self.usuario_emprestado = None
            self.data_emprestimo = None
            self.data_devolucao_prevista = None
            return True
        else:
            return False

    def calcular_prazo_emprestimo(self, usuario):
        
        if usuario.tipo == "Aluno Graduação":
            return 3
        elif usuario.tipo == "Aluno Pós-Graduação":
            return 4
        elif usuario.tipo == "Professor":
            return 7


    def consultar_status(self):
        return {
            "codigo_exemplar": self.codigo,
            "status": self.status,
            "usuario_emprestado": self.usuario_emprestado.nome if self.usuario_emprestado else None,
            "data_emprestimo": self.data_emprestimo.strftime("%Y-%m-%d %H:%M:%S") if self.data_emprestimo else None,
            "data_devolucao_prevista": self.data_devolucao_prevista.strftime("%Y-%m-%d %H:%M:%S")
            if self.data_devolucao_prevista
            else None,
        }

