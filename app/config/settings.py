import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")

# Preços por 1 milhão de tokens.
# Ajuste estes valores se mudar o modelo.
INPUT_PRICE_PER_MILLION = float(os.getenv("INPUT_PRICE_PER_MILLION", "0.20"))
OUTPUT_PRICE_PER_MILLION = float(os.getenv("OUTPUT_PRICE_PER_MILLION", "1.20"))
