from models.chamada import Chamada

chamadas = []

def registrar_chamada(turma_id, aluno_id, data, status):
    chamadas.append(Chamada(turma_id, aluno_id, data, status))

def historico_por_turma(turma_id):
    return [c for c in chamadas if c.turma_id == turma_id]