from time import sleep
from elasticsearch import Elasticsearch
import logging

# Configura o logger para mostrar mensagens informativas
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


exit("ATENÇÃO: tem que indicar o host e renomear o índice, adicione um suffixo com seu nome ou um numero, para não sobrescrever o índice de outro aluno.")
elastic_host = 'http://localhost:9200'
index_name='erbd-reviews-index-001'



logger.info("Este é um script de teste para o Elastic Search. Ele cria um índice (semelhante a uma tabela no postgres) chamado index_name e insere alguns reviews de celulares. Ele também faz uma busca por reviews que contenham a palavra 'celular'.")
sleep(5)

# Lista de reviews simulando dados reais
reviews = [
    {
        "id": 1,
        "text": "O celular é muito bom, a bateria dura bastante e a câmera é excelente.",
        "rating": 5
    },
    {
        "id": 2,
        "text": "Os celulares são muito bons, as baterias duram bastante e as câmeras são excelentes.",
        "rating": 5
    },
    {
        "id": 3,
        "text": "O celular é muito ruim, a bateria dura pouco e a câmera é péssima.",
        "rating": 1
    },
    {
        "id": 4,
        "text": "Os celulares são muito ruins, as baterias duram pouco e as câmeras são péssimas.",
        "rating": 1
    },
    {
        "id": 5,
        "text": "O celular é bom, a bateria dura bastante e a câmera é excelente.",
        "rating": 4
    },
    {
        "id": 6,
        "text": "Os celulares são bons, as baterias duram bastante e as câmeras são excelentes.",
        "rating": 4
    },
    {
        "id": 7,
        "text": "O celular é ruim, a bateria dura pouco e a câmera é péssima.",
        "rating": 2
    },
    {
        "id": 8,
        "text": "Os celulares são ruins, as baterias duram pouco e as câmeras são péssimas.",
        "rating": 2
    },
    {
        "id": 9,
        "text": "O celular é ótimo, a bateria dura bastante e a câmera é excelente.",
        "rating": 5
    },
    {
        "id": 10,
        "text": "Os celulares são ótimos, as baterias duram bastante e as câmeras são excelentes.",
        "rating": 5
    }
]

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