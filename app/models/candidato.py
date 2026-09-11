from dataclasses import dataclass


@dataclass
class Candidato:
    nome: str
    experiencia_anos: float
    pretensao_salarial: float
    aprovado: bool
    motivo: str = ""
