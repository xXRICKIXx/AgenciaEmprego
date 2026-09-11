import tiktoken
from openai import OpenAI

from app.config.settings import OPENAI_API_KEY, OPENAI_MODEL
from app.services.token_service import contar_tokens


SYSTEM_PROMPT = """
Você é um analista de recrutamento especializado em profissionais de tecnologia.

Analise o currículo fornecido de forma objetiva e profissional.

Retorne:
1. Um parecer qualitativo sobre a senioridade provável.
2. Soft skills que possam ser inferidas do currículo, deixando claro que são inferências.
3. Um resumo executivo curto para um recrutador.

Não invente experiências, tecnologias ou informações que não estejam no currículo.
""".strip()


def analisar_candidato(texto_curriculo: str) -> dict:
    if not OPENAI_API_KEY:
        raise RuntimeError(
            "OPENAI_API_KEY não configurada. Crie um arquivo .env "
            "a partir do .env.example."
        )

    client = OpenAI(api_key=OPENAI_API_KEY)

    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        "CURRÍCULO:\n"
        f"{texto_curriculo}\n\n"
        "FORMATO DA RESPOSTA:\n"
        "PARECER:\n"
        "...\n\n"
        "RESUMO:\n"
        "..."
    )

    # tiktoken é usado para monitoramento do consumo.
    # O uso exato retornado pela API também é capturado quando disponível.
    try:
        encoding = tiktoken.encoding_for_model(OPENAI_MODEL)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")

    estimativa_input = contar_tokens(prompt, encoding)

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt,
    )

    output_text = response.output_text

    usage = getattr(response, "usage", None)
    input_tokens = getattr(usage, "input_tokens", None) if usage else None
    output_tokens = getattr(usage, "output_tokens", None) if usage else None

    input_tokens = input_tokens or estimativa_input
    output_tokens = output_tokens or contar_tokens(output_text, encoding)

    parecer = output_text
    resumo = output_text

    if "RESUMO:" in output_text:
        parecer, resumo = output_text.split("RESUMO:", 1)
        parecer = parecer.replace("PARECER:", "").strip()
        resumo = resumo.strip()

    return {
        "parecer": parecer,
        "resumo": resumo,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "model": OPENAI_MODEL,
    }
