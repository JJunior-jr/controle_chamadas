from models.aluno import Aluno

alunos = []

def criar_aluno(nome, nascimento, telefone, foto_path, turma_id):
    novo = Aluno(id=len(alunos)+1, nome=nome, nascimento=nascimento, telefone=telefone, foto_path=foto_path, turma_id=turma_id)
    alunos.append(novo)
    return novo

def listar_alunos():
    return alunos

def listar_por_turma(turma_id):
    return [a for a in alunos if a.turma_id == turma_id]

def deletar_aluno(aluno_id):
    global alunos
    alunos = [a for a in alunos if a.id != aluno_id]