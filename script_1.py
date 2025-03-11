from elasticsearch import Elasticsearch

# criar um conjunto de dados de 10 reviews em portugues
# os reviews devem conter texto sobre produtos de celular
# devem ter pelo menos 100 caracteres cada
# quero que voce use plural e singular para mostrar o potencial do stemmer
# da busca do elastic search
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

# criar um indice no elastic search chamado 'erbd-reviews-index'
es = Elasticsearch(hosts=['http://localhost:9200'])

# mappings com indexação para brazilian portuguese
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
mappings = {
    "dynamic": "strict",
    "properties": {
        "id": {"type": "integer"},
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


if es.indices.exists(index='erbd-reviews-index'):
    es.indices.delete(index='erbd-reviews-index')

es.indices.create(index='erbd-reviews-index', mappings=mappings, settings=settings)

# inserir os reviews no indice
for review in reviews:
    es.index(index='erbd-reviews-index', body=review, refresh=True)

# buscar por reviews que contem a palavra 'celular'
query = {   
    "query_string": {
        "query": 'celular excelente',
        "fields": ["text"],
        "quote_field_suffix": ".exact"
    }
}

highlight = {
    "fields": {
        "text": {}
    }
}

result = es.search(index='erbd-reviews-index', query=query, highlight=highlight)

for hit in result['hits']['hits']:
    #print(hit['_source'], "score:", hit['_score'])
    print(hit.get('highlight', {}).get('text', []), "score:", hit['_score'])