# Agência de Empregos IA

Projeto desenvolvido para o Checkpoint 1 da disciplina de IA&ML do curso de Engenharia de Software.

## Descrição

Sistema de triagem automatizada de currículos de profissionais de tecnologia. O sistema recebe um currículo em PDF, extrai seu conteúdo, aplica filtros determinísticos de experiência e pretensão salarial e, somente para candidatos aprovados, realiza uma análise qualitativa com IA generativa. Também monitora tokens e estima o custo da execução.

## Objetivos

- Automatizar a triagem inicial de currículos.
- Extrair informações de currículos em PDF.
- Aplicar regras de negócio antes da utilização da IA.
- Evitar chamadas desnecessárias ao modelo generativo.
- Gerar parecer sobre senioridade e soft skills inferidas.
- Produzir resumo executivo para o recrutador.
- Monitorar tokens de entrada e saída.
- Estimar o custo de cada análise generativa.

## Fluxo do sistema

```text
Currículo PDF
     ↓
Extração do texto
     ↓
Filtros determinísticos
     ├── Reprovado → Finaliza a triagem
     └── Aprovado
             ↓
       Análise com IA
             ↓
   Parecer + resumo executivo
             ↓
   Tokens + custo estimado
             ↓
          Resultado
```

A análise generativa somente é realizada após a aprovação nos filtros determinísticos.

## Regras de negócio

### Experiência profissional

O sistema identifica a experiência informada no currículo e compara com o mínimo de anos exigido para a vaga.

### Pretensão salarial

O sistema identifica a pretensão salarial e compara com o orçamento máximo definido para a vaga.

Se o candidato não atender aos critérios obrigatórios, a triagem é encerrada sem realizar chamada ao modelo de IA.

## Análise generativa

Para candidatos aprovados, o sistema utiliza um modelo de linguagem para gerar:

- parecer sobre a senioridade provável;
- inferências sobre soft skills presentes no currículo;
- resumo executivo direcionado ao recrutador.

A análise é orientada para não inventar informações que não estejam presentes no currículo.

## Monitoramento de tokens

O sistema utiliza `tiktoken` para monitorar o consumo de tokens e captura os dados de uso retornados pela API quando disponíveis.

São apresentados:

- tokens de entrada;
- tokens de saída;
- total de tokens;
- modelo utilizado;
- custo estimado da execução.

Os preços utilizados no cálculo são configuráveis no `.env`.

## Tecnologias utilizadas

- **Python**
- **pypdf** — extração de texto de PDF
- **OpenAI API** — análise generativa
- **tiktoken** — contagem de tokens
- **python-dotenv** — variáveis de ambiente
- **Git/GitHub** — versionamento

## Estrutura do projeto

```text
agencia-empregos-ia/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── candidato.py
│   └── services/
│       ├── __init__.py
│       ├── pdf_service.py
│       ├── filtro_service.py
│       ├── ia_service.py
│       └── token_service.py
│
├── curriculos/
├── resultados/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── integrantes.txt
└── README.md
```

## Responsabilidade dos módulos

### `main.py`

Ponto de entrada da aplicação.

### `app/main.py`

Coordena o fluxo de triagem: entrada dos critérios, extração do PDF, filtros, análise com IA e relatório de tokens.

### `pdf_service.py`

Realiza a leitura dos arquivos PDF e extração do texto.

### `filtro_service.py`

Aplica as regras determinísticas de experiência e pretensão salarial.

### `candidato.py`

Define a estrutura de dados do candidato e do resultado dos filtros.

### `ia_service.py`

Realiza a comunicação com o modelo de IA e gera o parecer e o resumo executivo.

### `token_service.py`

Calcula o total de tokens e a estimativa de custo.

### `settings.py`

Centraliza as configurações obtidas por variáveis de ambiente.

## Instalação

Recomenda-se utilizar um ambiente virtual Python.

### Windows

```bash
python -m venv .venv
.venv\\Scripts\\activate
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Configuração da API

Copie `.env.example` para `.env` e configure sua chave da API:

```env
OPENAI_API_KEY=sua_chave_aqui
OPENAI_MODEL=seu_modelo
INPUT_PRICE_PER_MILLION=0.20
OUTPUT_PRICE_PER_MILLION=1.20
```

O arquivo `.env` não deve ser enviado ao GitHub.

## Execução

Com o ambiente virtual ativado:

```bash
python main.py
```

O programa solicitará:

```text
Informe o caminho do currículo PDF:
Experiência mínima exigida (anos):
Orçamento máximo da vaga (R$):
```

Exemplo:

```text
Informe o caminho do currículo PDF: curriculos/curriculo_candidato_demo.pdf
Experiência mínima exigida (anos): 3
Orçamento máximo da vaga (R$): 10000
```

## Exemplo de resultado

Um candidato com 5 anos de experiência e pretensão de R$ 8.500,00, para uma vaga que exige 3 anos e possui orçamento de R$ 10.000,00, deve passar pelos filtros e seguir para a análise generativa.

```text
RESULTADO: APROVADO NOS FILTROS
Enviando currículo para análise generativa...

--- PARECER DA IA ---
[parecer gerado pelo modelo]

--- RESUMO EXECUTIVO ---
[resumo gerado pelo modelo]

--- RELATÓRIO DE TOKENS ---
Modelo: [modelo utilizado]
Tokens de entrada: [quantidade]
Tokens de saída: [quantidade]
Total de tokens: [quantidade]
Custo estimado: US$ [valor]
```

## Candidato reprovado

Quando o candidato não atende aos critérios determinísticos, o sistema apresenta o motivo e encerra a triagem sem chamar a IA.

```text
RESULTADO: REPROVADO NA ETAPA DETERMINÍSTICA
Motivo: experiência abaixo do mínimo
```

## Segurança

- A chave da API é armazenada em variável de ambiente.
- `.env` está incluído no `.gitignore`.
- Currículos podem ser mantidos localmente na pasta `curriculos`.
- Não utilize dados pessoais reais sem autorização.

## Limitações

A extração é destinada principalmente a PDFs que possuem texto selecionável. Currículos compostos exclusivamente por imagens podem exigir OCR, que não faz parte do escopo atual.

A identificação automática de experiência e salário utiliza padrões de texto e pode depender da forma como as informações aparecem no currículo.

## Dependências

```text
openai
pypdf
tiktoken
python-dotenv
```

## Integrantes

Preencha nomes, RMs e link do repositório no arquivo `integrantes.txt`.

## Conclusão

O projeto demonstra uma abordagem híbrida de triagem de currículos, combinando regras determinísticas com inteligência artificial generativa. A separação das etapas permite avaliar critérios objetivos antes do uso da IA, reduzindo chamadas desnecessárias e possibilitando o monitoramento do consumo de tokens e do custo associado ao processamento.
