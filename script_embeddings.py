from time import sleep
from elasticsearch import Elasticsearch
import logging
from tqdm import tqdm
from config import elastic_host, index_name

# Configura o logger para mostrar mensagens informativas
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Lista de reviews simulando dados reais
from google_play_scraper import reviews, Sort

app_id = 'br.com.gabba.Caixa' # ID do aplicativo
result_list, continuation_token = reviews(
    app_id,
    lang='pt',
    country='br',
    sort=Sort.MOST_RELEVANT,
    count=100
)

reviews = []

logger.info("Conectando ao Elasticsearch local...")
es = Elasticsearch(hosts=[elastic_host])

logger.info("Definindo configurações de análise para o português brasileiro...")
settings = {
    "analysis": {
        "analyzer": {            
            "exact_analyzer": {
                "type": "custom",
                "tokenizer": "standard",                
                "filter": ["lowercase"]
            }
        },
    }
}

logger.info("Definindo mapeamento dos campos do índice...")
mappings = {
    "dynamic": "strict",
    "properties": {
        "id_review": {"type": "keyword"},
        "id": {"type": "keyword"},
        "text": {
            "type": "text",
            "analyzer": "brazilian",           
            "fields": {
                "exact": {
                    "type": "text",
                    "analyzer": "exact_analyzer"
                }                                
            }            
        },
        "sentence": {
            "type": "text",
            "analyzer": "brazilian",           
            "fields": {
                "exact": {
                    "type": "text",
                    "analyzer": "exact_analyzer"
                }                                
            }            
        },        
        "rating": {"type": "integer"},
        "sentence_embeddings": {
            "type": "dense_vector",
            "dims": 384,
            "index": True,
            "similarity": "cosine"
        }
    }
}

logger.info("Removendo o índice se já existir, para garantir um ambiente limpo...")
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

logger.info("Criando o índice com as configurações e mapeamentos definidos...")
es.indices.create(index=index_name, mappings=mappings, settings=settings)

logger.info("Inserindo cada review no índice...")
for review in reviews:
    es.index(index=index_name, body=review, refresh=True)


logger.info("Definindo a consulta para buscar reviews com as palavras 'aplicativo lento'...")
query_text = 'aplicativo lento'

query_vector = []
# mostrar os primeiros 10 valores do vetor ... e os ultimos 3, usar 4 casas decimais
logger.info(f"Vetor da consulta: {query_vector[:10]} ... {query_vector[-3:]}")

knn_query = {    
    "field": "sentence_embeddings",
    "query_vector": query_vector,
    "k": 20,
    "num_candidates": 100    
}

logger.info("Configurando o destaque (highlight) para mostrar os trechos encontrados...")

logger.info("Executando a busca no índice...")
result = es.search(index=index_name, knn=knn_query)

logger.info("Exibindo os resultados encontrados, mostrando o texto completo e a sentença e a pontuação...")
for hit in result['hits']['hits']:    
    logger.info(f"Score: {hit['_score']:.2f} - Texto: {hit['_source']['text']} - Sentença: {hit['_source']['sentence']} - Pontuação: {hit['_source']['rating']}")
    # sleep(0.5) # para não sobrecarregar o log, comentar se não precisar
    
    