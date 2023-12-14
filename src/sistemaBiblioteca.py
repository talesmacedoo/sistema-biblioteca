from livro import Livro
from usuario import Usuario, Observador, AlunoGraduacao, AlunoPos, Professor
from exemplar import Exemplar


class SistemaBiblioteca:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SistemaBiblioteca, cls).__new__(cls)
            cls._instance._livros = []
            cls._instance._usuarios = []
            cls._instance._observadores = []
        return cls._instance

    def cadastrar_livro(self, codigo, titulo, editora, autor, edicao, ano):
        livro = Livro(codigo, titulo, editora, autor, edicao, ano)
        self._livros.append(livro)
        return True, f"Livro '{titulo}' cadastrado com sucesso."

    def cadastrar_usuario(self, codigo, nome, tipo):
        tipos_usuarios = {
            "Aluno Graduação": AlunoGraduacao,
            "Aluno Pós-Graduação": AlunoPos,
            "Professor": Professor
        }

        usuario_cls = tipos_usuarios.get(tipo)
        if usuario_cls:
            usuario = usuario_cls(codigo, nome)
            self._usuarios.append(usuario)
            return True, f"Usuário '{nome}' cadastrado com sucesso."
        else:
            return False, "Tipo de usuário inválido"

    def registrar_observador(self, codigo_usuario, codigo_livro):
        usuario = self._encontrar_usuario_por_codigo(codigo_usuario)
        livro = self._encontrar_livro_por_codigo(codigo_livro)

        if usuario and livro:
            if isinstance(usuario, Professor):
                livro.adicionar_observador(usuario)
                return True, f"Professor {usuario.nome} registrado como observador do livro {livro.titulo}."
            else:
                return False, "Apenas professores podem ser registrados como observadores."
        else:
            return False, "Usuário ou livro não encontrado."

    def adicionar_exemplar(self, codigo_livro, codigo_exemplar):
        livro = self._encontrar_livro_por_codigo(codigo_livro)
        if livro:
            livro.adicionar_exemplar(codigo_exemplar)
            return True, f"Exemplar {codigo_exemplar} adicionado ao livro {livro.titulo}."
        else:
            return False, "Livro não encontrado."

    def realizar_emprestimo(self, codigo_usuario, codigo_livro):
        usuario = self._encontrar_usuario_por_codigo(codigo_usuario)
        livro = self._encontrar_livro_por_codigo(codigo_livro)

        if usuario and livro:
            resultado, mensagem = livro.realizar_emprestimo(usuario)
            if resultado:
                return True, f"Empréstimo realizado com sucesso para {usuario.nome} - Livro: {livro.titulo}"
            else:
                return False, f"Empréstimo não realizado para {usuario.nome} - Motivo: {mensagem}"
        else:
            return False, "Usuário ou livro não encontrado."

    def realizar_devolucao(self, codigo_usuario, codigo_livro):
        usuario = self._encontrar_usuario_por_codigo(codigo_usuario)
        livro = self._encontrar_livro_por_codigo(codigo_livro)

        if usuario and livro:
            emprestimo = self._encontrar_emprestimo_em_curso(usuario, livro)

            if emprestimo:
                sucesso, mensagem = emprestimo.realizar_devolucao()

                if sucesso:
                    usuario.emprestimos.remove(emprestimo)
                    return True, f"Devolução realizada com sucesso: {mensagem}"
                else:
                    return False, f"Devolução não realizada: {mensagem}"
            else:
                return False, "Usuário não possui empréstimo em curso para o livro especificado."
        else:
            return False, "Usuário ou livro não encontrado."

    def _encontrar_emprestimo_em_curso(self, usuario, livro):
        for emprestimo in usuario.emprestimos:
            if emprestimo.livro == livro and emprestimo.status == "Em curso":
                return emprestimo
        return None

    def realizar_reserva(self, codigo_usuario, codigo_livro):
        usuario = self._encontrar_usuario_por_codigo(codigo_usuario)
        livro = self._encontrar_livro_por_codigo(codigo_livro)

        if usuario and livro:
            if len(usuario.reservas) >= 3:
                return False, "Reserva não realizada. Limite de reservas atingido."

            if usuario.possui_reserva(livro):
                return False, "Reserva não realizada. Livro já reservado pelo usuário."

            if len(livro.exemplares_disponiveis()) > 0 or any(
                emprestimo.livro == livro and emprestimo.status == "Em curso" for emprestimo in usuario.emprestimos
            ):
                livro.realizar_reserva(usuario)
                return True, "Reserva realizada com sucesso."
        else:
            return False, "Reserva não realizada. Verifique as condições."

    def _encontrar_usuario_por_codigo(self, codigo_usuario):
        for usuario in self._usuarios:
            if usuario.codigo == codigo_usuario:
                return usuario
        return None

    def _encontrar_livro_por_codigo(self, codigo_livro):
        for livro in self._livros:
            if livro.codigo == codigo_livro:
                return livro
        return None

    def registrar_observador(self, codigo_usuario, codigo_livro):
        usuario = self._encontrar_usuario_por_codigo(codigo_usuario)
        livro = self._encontrar_livro_por_codigo(codigo_livro)

        if usuario and livro:
            livro.adicionar_observador(usuario)
            return True, "Observador registrado com sucesso."

        return False, "Observador não registrado. Verifique as condições."

    def consultar_livro(self, codigo_livro):
        livro = self._encontrar_livro_por_codigo(codigo_livro)

        if livro:
            info_livro = {
                "Título": livro.titulo,
                "Quantidade de Reservas": len(livro.reservas),
                "Exemplares": [
                    {
                        "Código": exemplar.codigo,
                        "Status": exemplar.status,
                        "Usuário que realizou o empréstimo": exemplar.usuario_emprestado.nome
                        if exemplar.usuario_emprestado
                        else None,
                        "Data de Empréstimo": exemplar.data_emprestimo.strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        if exemplar.data_emprestimo
                        else "Disponível",
                        "Data Prevista para Devolução": exemplar.data_prevista_devolucao.strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        if hasattr(exemplar, "data_prevista_devolucao")
                        and exemplar.data_prevista_devolucao
                        else None,
                    }
                    for exemplar in livro.exemplares
                ],
            }
            return True, info_livro
        else:
            return False, "Livro não encontrado."

    def consultar_usuario(self, codigo_usuario):
        usuario = self._encontrar_usuario_por_codigo(codigo_usuario)

        if usuario:
            info_usuario = {
                "Código": usuario.codigo,
                "Nome": usuario.nome,
                "Tipo": usuario.tipo,
                "Empréstimos Ativos": [
                    {
                        "Livro": emprestimo.livro.titulo,
                        "Data de Empréstimo": emprestimo.data_emprestimo.strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "Status": "Empréstimo Ativo"
                        if emprestimo.status == "Em curso"
                        else "Empréstimo Finalizado",
                    }
                    for emprestimo in usuario.emprestimos
                ],
                "Reservas": [livro.titulo for livro in usuario.reservas],
            }
            return True, info_usuario
        else:
            return False, "Usuário não encontrado."

    def consultar_notificacoes_professor(self, codigo_usuario):
        professor = self._encontrar_usuario_por_codigo(codigo_usuario)

        if isinstance(professor, Professor):
            num_notificacoes = professor.observacoes
            return True, f"O professor {professor.nome} foi notificado {num_notificacoes} vezes sobre mais de duas reservas simultâneas."
        else:
            return False, "Usuário não é um professor."





sistema = SistemaBiblioteca()

# livros
sistema.cadastrar_livro(codigo="100", titulo="Engenharia de Software", editora="AddisonWesley", autor="Ian Sommervile", edicao="6ª", ano="2000")
sistema.cadastrar_livro(codigo="101", titulo="UML – Guia do Usuário", editora="Campus", autor="Grady Booch, James Rumbaugh, Ivar Jacobson", edicao="7ª", ano="2000")
sistema.cadastrar_livro(codigo="200", titulo="Code Complete", editora="Microsoft Press", autor="Steve McConnell", edicao="2ª", ano="2014")
sistema.cadastrar_livro(codigo="201", titulo="Agile Software Development, Principles, Patterns, and Practices", editora="Prentice Hall", autor="Robert Martin", edicao="1ª", ano="2002")
sistema.cadastrar_livro(codigo="300", titulo="Refactoring: Improving the Design of Existing Code", editora="AddisonWesley Professional", autor="Martin Fowler", edicao="1ª", ano="1999")
sistema.cadastrar_livro(codigo="301", titulo="Software Metrics: A Rigorous and Practical Approach", editora="CRC Press", autor="Norman Fenton, James Bieman", edicao="3ª", ano="2014")
sistema.cadastrar_livro(codigo="400", titulo="Design Patterns: Elements of Reusable Object-Oriented Software", editora="AddisonWesley Professional", autor="Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides", edicao="1ª", ano="1994")
sistema.cadastrar_livro(codigo="401", titulo="UML Distilled: A Brief Guide to the Standard Object Modeling Language", editora="AddisonWesley Professional", autor="Martin Fowler", edicao="3ª", ano="2003")
# Eexemplares
sistema.adicionar_exemplar(codigo_livro="100", codigo_exemplar="1")
sistema.adicionar_exemplar(codigo_livro="100", codigo_exemplar="2")
sistema.adicionar_exemplar(codigo_livro="101", codigo_exemplar="3")
sistema.adicionar_exemplar(codigo_livro="200", codigo_exemplar="4")
sistema.adicionar_exemplar(codigo_livro="201", codigo_exemplar="5")
sistema.adicionar_exemplar(codigo_livro="300", codigo_exemplar="6")
sistema.adicionar_exemplar(codigo_livro="300", codigo_exemplar="7")
sistema.adicionar_exemplar(codigo_livro="400", codigo_exemplar="8")
sistema.adicionar_exemplar(codigo_livro="400", codigo_exemplar="9")
#usuários
sistema.cadastrar_usuario(codigo="123", nome="João da Silva", tipo="Aluno Graduação")
sistema.cadastrar_usuario(codigo="456", nome="Luiz Fernando Rodrigues", tipo="Aluno Pós-Graduação")
sistema.cadastrar_usuario(codigo="789", nome="Pedro Paulo", tipo="Aluno Graduação")
sistema.cadastrar_usuario(codigo="100", nome="Carlos Lucena", tipo="Professor")



