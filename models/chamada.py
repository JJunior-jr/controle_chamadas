from dataclasses import dataclass
from datetime import date

@dataclass
class Chamada:
    turma_id: int
    aluno_id: int
    data: date
    status: str  # "Presente" ou "Falta"S