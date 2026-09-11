from pathlib import Path

from app.services.pdf_service import extrair_texto_pdf
from app.services.filtro_service import aplicar_filtros
from app.services.ia_service import analisar_candidato
from app.services.token_service import gerar_relatorio_tokens


def executar_triagem():
    print("=" * 60)
    print("AGÊNCIA DE EMPREGOS IA - TRIAGEM DE CURRÍCULOS")
    print("=" * 60)

    caminho = input("Informe o caminho do currículo PDF: ").strip()
    experiencia_minima = float(input("Experiência mínima exigida (anos): "))
    salario_maximo = float(input("Orçamento máximo da vaga (R$): "))

    pdf = Path(caminho)
    if not pdf.exists() or pdf.suffix.lower() != ".pdf":
        print("Arquivo PDF não encontrado ou extensão inválida.")
        return

    try:
        texto = extrair_texto_pdf(pdf)
        candidato = aplicar_filtros(texto, experiencia_minima, salario_maximo)

        print(f"\nCandidato: {candidato.nome}")
        print(f"Experiência identificada: {candidato.experiencia_anos:.1f} anos")
        print(f"Pretensão salarial: R$ {candidato.pretensao_salarial:,.2f}")

        if not candidato.aprovado:
            print("\nRESULTADO: REPROVADO NA ETAPA DETERMINÍSTICA")
            print(f"Motivo: {candidato.motivo}")
            return

        print("\nRESULTADO: APROVADO NOS FILTROS")
        print("Enviando currículo para análise generativa...")

        analise = analisar_candidato(texto)
        print("\n--- PARECER DA IA ---")
        print(analise["parecer"])
        print("\n--- RESUMO EXECUTIVO ---")
        print(analise["resumo"])

        relatorio = gerar_relatorio_tokens(
            analise["input_tokens"],
            analise["output_tokens"],
            analise["model"]
        )

        print("\n--- RELATÓRIO DE TOKENS ---")
        print(f"Modelo: {relatorio['modelo']}")
        print(f"Tokens de entrada: {relatorio['input_tokens']}")
        print(f"Tokens de saída: {relatorio['output_tokens']}")
        print(f"Total de tokens: {relatorio['total_tokens']}")
        print(f"Custo estimado: US$ {relatorio['custo_usd']:.8f}")

    except Exception as exc:
        print(f"\nErro durante a triagem: {exc}")
