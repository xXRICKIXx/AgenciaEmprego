import re
from app.models.candidato import Candidato


def _buscar_numero(texto: str, padroes, default=0.0):
    for padrao in padroes:
        match = re.search(padrao, texto, re.IGNORECASE)
        if match:
            return float(match.group(1).replace(",", "."))
    return default


def _buscar_salario(texto: str) -> float:
    padroes = [
        r"(?:pretens[aã]o|pretens[aã]o salarial|sal[aá]rio desejado)[^\d]{0,30}"
        r"(?:r\$)?\s*([\d.,]+)",
        r"(?:salary expectation|expected salary)[^\d]{0,30}"
        r"(?:r\$)?\s*([\d.,]+)",
    ]

    for padrao in padroes:
        match = re.search(padrao, texto, re.IGNORECASE)
        if match:
            valor = match.group(1).replace(".", "").replace(",", ".")
            return float(valor)

    return 0.0


def _buscar_experiencia(texto: str) -> float:
    padroes = [
        r"(\d+(?:[.,]\d+)?)\s*\+?\s*anos?\s+de\s+experi[eê]ncia",
        r"experi[eê]ncia\s*(?:profissional)?[^\d]{0,20}"
        r"(\d+(?:[.,]\d+)?)\s*anos?",
        r"(\d+(?:[.,]\d+)?)\s*years?\s+of\s+experience",
    ]
    return _buscar_numero(texto, padroes)


def _buscar_nome(texto: str) -> str:
    for linha in texto.splitlines():
        linha = linha.strip()
        if linha and len(linha.split()) >= 2 and len(linha) < 80:
            return linha
    return "Candidato não identificado"


def aplicar_filtros(
    texto: str,
    experiencia_minima: float,
    salario_maximo: float
) -> Candidato:
    nome = _buscar_nome(texto)
    experiencia = _buscar_experiencia(texto)
    salario = _buscar_salario(texto)

    motivos = []

    if experiencia < experiencia_minima:
        motivos.append(
            f"experiência abaixo do mínimo ({experiencia:.1f} < {experiencia_minima:.1f} anos)"
        )

    # Salário 0 significa que a informação não foi encontrada.
    # Nesse caso, não reprovamos automaticamente.
    if salario > 0 and salario > salario_maximo:
        motivos.append(
            f"pretensão salarial acima do orçamento "
            f"(R$ {salario:,.2f} > R$ {salario_maximo:,.2f})"
        )

    aprovado = not motivos

    return Candidato(
        nome=nome,
        experiencia_anos=experiencia,
        pretensao_salarial=salario,
        aprovado=aprovado,
        motivo="; ".join(motivos)
    )
