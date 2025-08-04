from dataclasses import dataclass
from datetime import date

@dataclass
class Aluno:
    id: int
    nome: str
    nascimento: date
    telefone: str
    foto_path: str
    turma_id: int