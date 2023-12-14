from command import Command
from consultaLivro import ConsultaLivro
from consultaNotificacoesProfessor import ConsultaNotificacoesProfessor
from consultaUsuario import ConsultaUsuario
from realizarDevolucao import RealizarDevolucao
from realizarEmprestimo import RealizarEmprestimo
from realizarReserva import RealizarReserva
from registrarObeservador import RegistrarObservador
from sair import Sair
from sistemaBiblioteca import SistemaBiblioteca


class EntradaDados:

  def __init__(self):
    self.sistema = SistemaBiblioteca()

  def executar_comando(self, comando):
    return comando.execute()


def imprimir_resultado(resultado):
  if resultado[0]:
    print(resultado[1])
  else:
    print(f"Erro: {resultado[1]}")


facade = EntradaDados()
while True:
  entrada = input().split()
  comando_str = entrada[0].lower()
  comandos = {
      'sai': Sair,
      'liv': ConsultaLivro,
      'usu': ConsultaUsuario,
      'ntf': ConsultaNotificacoesProfessor,
      'emp': RealizarEmprestimo,
      'dev': RealizarDevolucao,
      'res': RealizarReserva,
      'obs': RegistrarObservador,
  }

  if comando_str not in comandos:
    print(f"Comando inválido: {comando_str}")
    continue

  comando = comandos[comando_str](facade.sistema, *entrada[1:])

  resultado = facade.executar_comando(comando)
  imprimir_resultado(resultado)
