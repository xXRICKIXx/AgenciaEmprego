from pathlib import Path
from pypdf import PdfReader


def extrair_texto_pdf(caminho: Path) -> str:
    reader = PdfReader(str(caminho))
    paginas = []

    for pagina in reader.pages:
        texto = pagina.extract_text() or ""
        if texto.strip():
            paginas.append(texto.strip())

    texto_final = "\n".join(paginas).strip()

    if not texto_final:
        raise ValueError(
            "Não foi possível extrair texto do PDF. "
            "Verifique se o currículo contém texto selecionável."
        )

    return texto_final
