from models.turma import Turma

turmas = []

def criar_turma(nome, descricao, inicio, fim):
    nova = Turma(id=len(turmas)+1, nome=nome, descricao=descricao, data_inicio=inicio, data_fim=fim)
    turmas.append(nova)
    return nova

def listar_turmas():
    return turmas

def deletar_turma(turma_id):
    global turmas
    turmas = [t for t in turmas if t.id != turma_id]