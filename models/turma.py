from dataclasses import dataclass
from datetime import date

@dataclass
class Turma:
    id: int
    nome: str
    descricao: str
    data_inicio: date
    data_fim: date
