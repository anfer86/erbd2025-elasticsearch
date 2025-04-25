from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from elasticsearch import Elasticsearch
import logging
from config import elastic_host, index_name

es = Elasticsearch(hosts=[elastic_host])    

app = FastAPI()

# Monta a pasta de assets para servir arquivos estáticos (ex: CSS)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def search_reviews(query_text):
    """Executa a busca no Elasticsearch e retorna os resultados formatados."""
    results = []
    query = {
        "query_string": {
            "query": query_text,
            "default_field": "text",            
        }
    }
    highlight = {"fields": {"text": {}}}
    
    
    es_result = es.search(index=index_name, query=query, highlight=highlight, size=20)
    for hit in es_result['hits']['hits']:
        results.append({
            "text": hit['_source']['text'],
            "rating": hit['_source']['rating'],
            "highlight": hit.get('highlight', {}).get('text', []),
            "score": round(hit['_score'], 2)
        })
    return results


@app.get('/', response_class=HTMLResponse)
def home(request: Request, q: str = ""):
    logger.info(f"Recebida consulta: {q}")
    results = []
    total = 0    
    if q:
        results = search_reviews(q)
        total = len(results)        
    # HTML com Bootstrap e estilo embutido
    html = f'''
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Busca de Reviews</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="/assets/style.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <div class="container py-5">
            <h1 class="mb-4">Buscar Reviews</h1>
            <form method="get" action="/">
                <div class="input-group mb-3">
                    <input type="text" class="form-control" name="q" value="{q}" placeholder="Digite sua busca..." required>
                    <button class="btn btn-primary" type="submit">Buscar</button>
                </div>
            </form>
            {'<h2 class="mt-4">Resultados:</h2>' if q else ''}
            {f'<p><b>Total de resultados encontrados:</b> {total}' if q else ''}
            <ul class="list-group">
                {''.join(f'<li class="list-group-item review"><b>Rating:</b> {r["rating"]}<br><b>Review:</b> {r["text"]}<br><b>Destaque:</b> {", ".join(r["highlight"]) if isinstance(r["highlight"], list) else r["highlight"]}<br><b>Score:</b> {r["score"]}</li>' for r in results)}
            </ul>
            {('<p class="mt-3">Nenhum resultado encontrado.</p>' if q and not results else '')}
        </div>
    </body>
    </html>
    '''
    return HTMLResponse(content=html)


# init
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)