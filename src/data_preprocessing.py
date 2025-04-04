"""
Módulo para processamento de dados do projeto de predição de preços de imóveis.
Realiza todas as etapas de limpeza, transformação e preparação dos dados.
"""
import pandas as pd
import numpy as np
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def carregar_dados(caminho_arquivo):
    """
    Carrega os dados a partir do arquivo CSV.
    
    Args:
        caminho_arquivo: Caminho para o arquivo CSV
        
    Returns:
        DataFrame com os dados carregados
    """
    logger.info("Carregando dados de %s", caminho_arquivo)
    return pd.read_csv(caminho_arquivo)

def limpar_dados(df):
    """
    Remove valores inválidos e outliers extremos.
    
    Args:
        df: DataFrame a ser limpo
        
    Returns:
        DataFrame limpo
    """
    logger.info("Limpando dados")
    df_limpo = df.copy()
    
    # Remover valores negativos em colunas que não podem ser negativas
    colunas_positivas = ['total_rooms', 'total_bedrooms', 'population', 'households', 'median_income']
    for coluna in colunas_positivas:
        if coluna in df_limpo.columns:
            df_limpo = df_limpo[df_limpo[coluna] >= 0]
    
    
    logger.info("Limpeza concluída. Restaram %d de %d registros.", len(df_limpo), len(df))
    return df_limpo

def tratar_valores_nulos(df):
    """
    Trata valores nulos no DataFrame.
    
    Args:
        df: DataFrame com possíveis valores nulos
        
    Returns:
        DataFrame sem valores nulos
    """
    logger.info("Tratando valores nulos")
    df_sem_nulos = df.copy()
    
    # Verificar colunas com valores nulos
    colunas_com_nulos = df_sem_nulos.columns[df_sem_nulos.isnull().any()].tolist()
    
    if colunas_com_nulos:
        logger.info("Colunas com valores nulos: %s", colunas_com_nulos)
        
        # Preencher valores nulos nas colunas numéricas com a mediana
        colunas_numericas = df_sem_nulos.select_dtypes(include=['number']).columns
        for coluna in colunas_com_nulos:
            if coluna in colunas_numericas:
                logger.info("Preenchendo valores nulos em %s com a mediana", coluna)
                df_sem_nulos[coluna] = df_sem_nulos[coluna].fillna(df_sem_nulos[coluna].median())
            else:
                # Para colunas categóricas, preencher com o valor mais frequente
                logger.info("Preenchendo valores nulos em %s com o valor mais frequente", coluna)
                df_sem_nulos[coluna] = df_sem_nulos[coluna].fillna(df_sem_nulos[coluna].mode()[0])
    else:
        logger.info("Não foram encontrados valores nulos no DataFrame")
    
    return df_sem_nulos

def processar_categorias(df):
    """
    Processa variáveis categóricas para formato adequado para modelagem.
    
    Args:
        df: DataFrame com variáveis categóricas
        
    Returns:
        DataFrame com variáveis categóricas processadas
    """
    logger.info("Processando variáveis categóricas")
    df_processado = df.copy()
    
    # Verificar se existe a coluna ocean_proximity
    if 'ocean_proximity' in df_processado.columns:
        logger.info("Aplicando one-hot encoding em ocean_proximity")
        # Criar variáveis dummy (one-hot encoding)
        df_dummies = pd.get_dummies(df_processado['ocean_proximity'], prefix='ocean_proximity')
        
        # Garantir que os valores sejam inteiros (0 ou 1)
        for coluna in df_dummies.columns:
            df_dummies[coluna] = df_dummies[coluna].astype(int)
            logger.info("Convertendo %s para valores 0/1", coluna)
        
        # Concatenar as dummies com o DataFrame original
        df_processado = pd.concat([df_processado, df_dummies], axis=1)
        
        # Remover a coluna original
        df_processado = df_processado.drop(columns=['ocean_proximity'])
        
        logger.info("Criadas %d colunas dummies para ocean_proximity com valores 0/1", len(df_dummies.columns))
    
    return df_processado

def adicionar_features(df):
    """
    Adiciona features derivadas para melhorar o poder preditivo.
    
    Args:
        df: DataFrame original
        
    Returns:
        DataFrame com novas features
    """
    logger.info("Adicionando features derivadas")
    df_features = df.copy()
    
    # Calcular features derivadas
    if all(coluna in df_features.columns for coluna in ['total_rooms', 'households']):
        df_features['rooms_per_household'] = df_features['total_rooms'] / df_features['households']
        # Corrigir valores infinitos
        df_features['rooms_per_household'] = df_features['rooms_per_household'].replace([np.inf, -np.inf], np.nan)
        df_features['rooms_per_household'] = df_features['rooms_per_household'].fillna(df_features['rooms_per_household'].median())
    
    if all(coluna in df_features.columns for coluna in ['total_bedrooms', 'households']):
        df_features['bedrooms_per_household'] = df_features['total_bedrooms'] / df_features['households']
        # Corrigir valores infinitos
        df_features['bedrooms_per_household'] = df_features['bedrooms_per_household'].replace([np.inf, -np.inf], np.nan)
        df_features['bedrooms_per_household'] = df_features['bedrooms_per_household'].fillna(df_features['bedrooms_per_household'].median())
    
    if all(coluna in df_features.columns for coluna in ['total_bedrooms', 'total_rooms']):
        df_features['bedrooms_per_room'] = df_features['total_bedrooms'] / df_features['total_rooms']
        # Corrigir valores infinitos
        df_features['bedrooms_per_room'] = df_features['bedrooms_per_room'].replace([np.inf, -np.inf], np.nan)
        df_features['bedrooms_per_room'] = df_features['bedrooms_per_room'].fillna(df_features['bedrooms_per_room'].median())
    
    if all(coluna in df_features.columns for coluna in ['population', 'households']):
        df_features['population_per_household'] = df_features['population'] / df_features['households']
        # Corrigir valores infinitos
        df_features['population_per_household'] = df_features['population_per_household'].replace([np.inf, -np.inf], np.nan)
        df_features['population_per_household'] = df_features['population_per_household'].fillna(df_features['population_per_household'].median())
    
    if 'median_income' in df_features.columns:
        df_features['median_income_squared'] = df_features['median_income'] ** 2
    
    logger.info("Adicionadas %d novas features", len(df_features.columns) - len(df.columns))
    return df_features

def preprocessar_dados(caminho_entrada, caminho_saida=None):
    """
    Executa o pipeline completo de processamento de dados.
    
    Args:
        caminho_entrada: Caminho para o arquivo de dados de entrada
        caminho_saida: Caminho para salvar os dados processados (opcional)
        
    Returns:
        DataFrame processado
    """
    # Carregar dados
    df = carregar_dados(caminho_entrada)
    
    # Aplicar etapas de processamento
    df = limpar_dados(df)
    df = tratar_valores_nulos(df)
    df = processar_categorias(df)
    df = adicionar_features(df)
    
    # Salvar dados processados, se especificado
    if caminho_saida:
        logger.info("Salvando dados processados em %s", caminho_saida)
        df.to_csv(caminho_saida, index=False)
    
    return df

if __name__ == "__main__":
    # Exemplo de uso
    projeto_dir = Path(__file__).resolve().parents[1]
    caminho_entrada = projeto_dir / "data" / "raw" / "housing.csv"
    caminho_saida = projeto_dir / "data" / "processed" / "housing_processed.csv"
    
    df_final = preprocessar_dados(caminho_entrada, caminho_saida)