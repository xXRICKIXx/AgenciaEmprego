from app.config.settings import (
    INPUT_PRICE_PER_MILLION,
    OUTPUT_PRICE_PER_MILLION,
)


def contar_tokens(texto: str, encoding) -> int:
    return len(encoding.encode(texto))


def calcular_custo(input_tokens: int, output_tokens: int) -> float:
    custo_input = (input_tokens / 1_000_000) * INPUT_PRICE_PER_MILLION
    custo_output = (output_tokens / 1_000_000) * OUTPUT_PRICE_PER_MILLION
    return custo_input + custo_output


def gerar_relatorio_tokens(input_tokens: int, output_tokens: int, model: str):
    return {
        "modelo": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "custo_usd": calcular_custo(input_tokens, output_tokens),
    }
