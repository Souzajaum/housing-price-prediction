﻿# Projeto de Predição de Preços de Habitação na Califórnia

Este projeto visa desenvolver um modelo de predição para preços de habitações na Califórnia baseado nos dados do censo de 1990, com foco em simplicidade e eficiência no código.

## Estrutura do Projeto

```
.
├── data/                      # Dados do projeto
│   ├── raw/                   # Dados brutos
│   │   └── housing.csv        # Dados originais
│   ├── intermediate/          # Dados intermediários
│   │   └── houses_with_urbanized_status.csv  # Dados com status de urbanização
│   └── processed/             # Dados processados
│       └── housing_processed.csv # Dados finais para modelagem
├── figures/                   # Visualizações geradas
├── models/                    # Modelos treinados e testados
├── notebooks/                 # Jupyter notebooks para análise exploratória
├── earth-engine/              # Scripts e dados relacionados ao Google Earth Engine
├── src/                       # Código-fonte
│   ├── data_preprocessing.py  # Processamento de dados principal
│   └── data_wrangling.py      # Funções auxiliares para manipulação de dados
└── README.md                  # Documentação
```

## Features do Projeto

### Features Originais
- `longitude` e `latitude`: localização geográfica
- `housing_median_age`: idade mediana das habitações
- `total_rooms`: número total de cômodos
- `total_bedrooms`: número total de quartos
- `population`: população total
- `households`: número de domicílios
- `median_income`: renda mediana (em dezenas de milhares de dólares)
- `median_house_value`: valor mediano das habitações (variável alvo)
- `ocean_proximity`: proximidade ao oceano (convertida para variáveis dummy 0/1)

### Features Derivadas
Para melhorar a capacidade preditiva, adicionamos as seguintes features:

1. **rooms_per_household**: número médio de cômodos por domicílio
2. **bedrooms_per_household**: número médio de quartos por domicílio
3. **bedrooms_per_room**: proporção de quartos em relação ao total de cômodos
4. **population_per_household**: população média por domicílio
5. **median_income_squared**: renda mediana ao quadrado (captura relações não-lineares)

## Como Usar

### Requisitos

Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

### Processamento de Dados

Para processar os dados:

```bash
python src/data_preprocessing.py
```

O script realiza as seguintes etapas:
1. Carrega os dados brutos
2. Remove valores inválidos e outliers
3. Trata valores nulos
4. Processa variáveis categóricas (converte `ocean_proximity` em variáveis dummy 0/1)
5. Adiciona features derivadas
6. Salva os dados processados

### Análise Exploratória de Dados

Para realizar uma análise exploratória completa:

```bash
python src/analise_exploratoria.py
```

Este script gera visualizações e insights sobre os dados, incluindo:
- Estatísticas descritivas
- Distribuição das variáveis
- Matriz de correlação
- Relações bivariadas com a variável alvo
- Análise espacial dos dados

As visualizações são salvas na pasta `figuras/`.

### Processamento de Dados de Urbanização

Para processar os dados de urbanização:

```bash
python src/process_urbanized.py
```

Este script processa o arquivo `houses_with_urbanized_status.csv`:
1. Remove a coluna `system:index`
2. Extrai latitude e longitude da coluna `.geo`
3. Salva um novo arquivo com as coordenadas extraídas

## Fluxo de Trabalho

1. **Preparação dos Dados**: Use `process_urbanized.py` para processar os dados de urbanização
2. **Processamento**: Execute `data_preprocessing.py` para preparar os dados para modelagem
3. **Análise**: Execute `analise_exploratoria.py` para entender os dados e identificar padrões
4. **Modelagem**: Utilize os dados processados para construir modelos preditivos

## Logs e Mensagens

O projeto utiliza o módulo de logging do Python para registrar informações sobre o processamento:

- Mensagens de **INFO**: mostram o progresso normal do processamento
- Mensagens de **WARNING**: indicam situações potencialmente problemáticas
- Mensagens de **ERROR**: reportam erros que impedem a conclusão de uma tarefa

Você pode ajustar o nível de logging conforme necessário.

## Autores

[Seu Nome]


