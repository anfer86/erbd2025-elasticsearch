from time import sleep
from elasticsearch import Elasticsearch
import logging

# Configura o logger para mostrar mensagens informativas
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#exit("ATENÇÃO: tem que indicar o host e renomear o índice, adicione um suffixo com seu nome ou um numero, para não sobrescrever o índice de outro aluno.")
elastic_host = 'http://localhost:9200'
index_name='erbd-reviews-index-001'

# Lista de reviews simulando dados reais
reviews = []

logger.info("Conectando ao Elasticsearch local...")
es = Elasticsearch(hosts=['http://localhost:9200'])

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
        "rating": {"type": "integer"}
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

logger.info("Definindo a consulta para buscar reviews com as palavras 'celular' e 'excelente'...")
query = {   
    "query_string": {
        "query": 'celular excelente',
        "fields": ["text"],
        "quote_field_suffix": ".exact"
    }
}

logger.info("Configurando o destaque (highlight) para mostrar os trechos encontrados...")
highlight = {
    "fields": {
        "text": {}
    }
}

logger.info("Executando a busca no índice...")
result = es.search(index=index_name, query=query, highlight=highlight)

logger.info("Exibindo os resultados encontrados, mostrando o trecho destacado e a pontuação...")
for hit in result['hits']['hits']:    
    logger.info(f"{hit.get('highlight', {}).get('text', [])} - Pontuação: {hit['_source']['rating']}")