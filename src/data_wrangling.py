"""
Script para processar o arquivo houses_with_urbanized_status.csv.
Extrai latitude e longitude da coluna .geo e remove colunas desnecessárias.
"""
import pandas as pd
import json
import logging
from pathlib import Path

#  logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def processar_coordenadas(geo_str):
    """
    Extrai latitude e longitude da string JSON da coluna .geo.
    
    Args:
        geo_str: String contendo o JSON com as coordenadas
        
    Returns:
        tuple: (longitude, latitude) com 2 casas decimais
    """
    try:
        geo_dict = json.loads(geo_str)
        coords = geo_dict['coordinates']
        return round(coords[0], 2), round(coords[1], 2)
    except Exception as e:
        logger.error("Erro ao processar coordenadas: %s", str(e))
        return None, None

def processar_arquivo_urbanized(caminho_entrada, caminho_saida):
    """
    Processa o arquivo houses_with_urbanized_status.csv.
    
    Args:
        caminho_entrada: Caminho para o arquivo de entrada
        caminho_saida: Caminho para salvar o arquivo processado
    """
    logger.info("Carregando arquivo de entrada: %s", caminho_entrada)
    df = pd.read_csv(caminho_entrada)
    
    # remoção da coluna system:index se existir
    if 'system:index' in df.columns:
        logger.info("Removendo coluna system:index")
        df = df.drop(columns=['system:index'])
    
    # extrair coordenadas da coluna .geo
    if '.geo' in df.columns:
        logger.info("Extraindo coordenadas da coluna .geo")
        # aplicar a função de processamento em cada linha
        coords = df['.geo'].apply(processar_coordenadas)
        
        # separar longitude e latitude em colunas diferentes
        df['longitude'] = coords.apply(lambda x: x[0] if x else None)
        df['latitude'] = coords.apply(lambda x: x[1] if x else None)
        
        # remoção da coluna .geo
        df = df.drop(columns=['.geo'])
        
        # verificação de valores nulos
        nulos = df['longitude'].isna().sum()
        if nulos > 0:
            logger.warning("Encontrados %d registros com coordenadas inválidas", nulos)
    else:
        logger.error("Coluna .geo não encontrada no arquivo")
        return
    
    # salvar arquivo processado
    logger.info("Salvando arquivo processado em: %s", caminho_saida)
    df.to_csv(caminho_saida, index=False)
    logger.info("Processamento concluído. Total de registros: %d", len(df))

if __name__ == "__main__":
    projeto_dir = Path(__file__).resolve().parents[1]
    caminho_entrada = projeto_dir / "data" / "intermediate" / "houses_with_urbanized_status.csv"
    caminho_saida = projeto_dir / "data" / "processed" / "housing_final.csv"
    
    processar_arquivo_urbanized(caminho_entrada, caminho_saida) 