from datetime import datetime, timedelta
from usuario import Usuario, AlunoGraduacao, AlunoPos, Professor
#from livro import Livro

class Emprestimo:
    def __init__(self, usuario, livro, exemplar):
        self.usuario = usuario
        self.livro = livro
        self.exemplar = exemplar
        self.data_emprestimo = datetime.now()
        self.data_devolucao_prevista = None
        self.status = "Em curso"

    def realizar_emprestimo(self):
        """ metodo para verificar as codições de emprestimo, caso sejam satisfeitas, adcionar dados no registro"""
        if self.verificar_condicoes_emprestimo():
            self.livro.emprestimos.append(self)
            self.usuario.emprestimos.append(self)
            return True, "Empréstimo realizado com sucesso."
        else:
            return False, "Empréstimo não realizado. Verifique as condições."

    def verificar_condicoes_emprestimo(self):
        
        exemplares_disponiveis = self.livro.exemplares_disponiveis()
        if exemplares_disponiveis == 0:
            return False



        if isinstance(self.usuario, AlunoGraduacao) and len(self.usuario.emprestimos) >= 3:
            return False
        elif isinstance(self.usuario, AlunoPos) and len(self.usuario.emprestimos) >= 4:
            return False
        
        if len(self.livro.reservas) >= exemplares_disponiveis and self.usuario not in self.livro.reservas:
            return False
        
        
        #Verifica se o usuário possui algum empréstimo em curso do mesmo livro
        if any(emprestimo.livro == self.livro and emprestimo.status == "Em curso" for emprestimo in self.usuario.emprestimos):
            return False
        return True



    def realizar_devolucao(self):
        #Atualiza o status do empréstimo durante a devolução
        if self.status == "Em curso":
            self.status = "Finalizado"
            exemplar_devolvido = self.exemplar
            exemplar_devolvido.devolver()
            return True, ""
        else:
            return False, " O empréstimo já foi finalizado."