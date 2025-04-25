# ElasticSearch na Prática: Busca Textual e Semântica com Embeddings

Este repositório contém os materiais da oficina **"ElasticSearch na prática: Busca Textual e Semântica com Embeddings"**, apresentada na **Escola Regional de Banco de Dados (ERBD) 2025**.

## Descrição

Nesta oficina, exploraremos como estruturar buscas utilizando ElasticSearch, desde consultas textuais tradicionais até buscas semânticas com embeddings. Vamos instanciar localmente um ambiente com ElasticSearch e Kibana via Docker, criar um índice e indexar dados reais de reviews usando Python. A partir disso, compararemos buscas sintáticas e semânticas, demonstrando como embeddings podem aprimorar a relevância dos resultados.

Essa é uma oportunidade prática para entender e aplicar técnicas modernas de busca de informação em grandes conjuntos de dados textuais, e como integrar essas técnicas em processos de **Retrieval-Augmented Generation (RAG)**, essencial para melhorar as respostas geradas pelos atuais modelos de linguagem.

## Requisitos

* Computador com possibilidade de rodar **Docker**
* IDE para ElasticSearch (ex.: Kibana, Postman, DevTools do Chrome)
* **Python** instalado para execução de scripts
* Editor de texto ou IDE (ex.: VSCode, PyCharm)

## A. Instalação e Configuração

### 1. Baixar o repositório sem Git

Se você não pode usar o Git, siga estes passos:

1. Acesse o site do projeto no GitHub: https://github.com/seu-usuario/elastic-search-erbd-2025
2. Clique no botão verde "Code" e selecione "Download ZIP".
3. Extraia o arquivo ZIP na sua Área de Trabalho.
4. Abra o VS Code e selecione "Abrir Pasta", escolhendo a pasta extraída.

### 1. a. Clonar este repositório com Git
```bash
$ git clone https://github.com/seu-usuario/elastic-search-erbd-2025.git
$ cd elastic-search-erbd-2025
```
Depois disso você pode abrir o VS Code e selecionar "Abrir Pasta", escolhendo a pasta do repositório clonado.

As etapas 2 e 3 são opcionais se você esta fazendo a oficina no ambiente do evento, pois o ElasticSearch e o Kibana já estão configuradas em `http://oficinaerbd.inf.ufsc.br:9200/` e `http://oficinaerbd.inf.ufsc.br:5601/`, respectivamente. Caso contrário, siga os passos abaixo para configurar o ambiente localmente.

### 2. Subir o ambiente com ElasticSearch e Kibana

Kibana é uma interface gráfica para interagir com o ElasticSearch. Para subir o ambiente, utilize o Docker Compose.

```bash
$ docker-compose up -d
```

Isso iniciará:
```bash
- **ElasticSearch** na porta `9200`
- **Kibana** na porta `5601`
```

Acesse o Kibana em: [http://localhost:5601](http://localhost:5601)

### 3. Verificar se o ElasticSearch está rodando

```bash
$ curl -X GET "http://localhost:9200/_cat/health?v"
```
Se estiver tudo certo, a resposta deve indicar que o status está `green` ou `yellow`.

### 4. Criar e ativar um ambiente virtual Python

Para isolar as dependências do projeto, criamos um ambiente virtual:
```bash
$ python -m venv env
```

Se o VSCode não detectar automaticamente o ambiente virtual, você pode ativá-lo manualmente.

No Windows, ative com:
```bash
$ env\Scripts\activate.bat
```
No Linux/macOS, ative com:
```bash
$ source env/bin/activate
```

### 5. Instalar as dependências

Instale os pacotes necessários listados no `requirements.txt`:
```bash
$ pip install -r requirements.txt
```
Este processo pode demorar alguns minutos, dependendo da sua conexão com a internet.

## Executando Scripts de Indexação

Para rodar o primeiro script de indexação, execute:
```bash
$ python script_test.py
```

## B. Entendendo o Script de Teste:

Após rodar o `script_test.py`, um índice chamado `erbd-reviews-index` é criado no ElasticSearch com alguns reviews de celulares. Agora, vamos explorar esse índice usando o Kibana:

- **Listar documentos:**  
  No Kibana, acesse o menu "Dev Tools" e execute:
  ```
  GET erbd-reviews-index/_search
  ```
  Isso retorna todos os documentos do índice.

- **Pesquisar documentos por texto:**  
  Para buscar reviews que contenham uma palavra específica, por exemplo "bateria":
  ```
  GET erbd-reviews-index/_search
  {
    "query": {
      "query_string": {
        "query": "bateria"
      }
    }
  }
  ```

  Observar o indice `GET erbd-reviews-index` e a configuração do mapeamento.

  Exemplo de teste do analyzer
  ```
  GET erbd-reviews-index/_analyze
  {
    "analyzer": "brazilian",
    "text": "baterias"
  }
  ```

  Pesquisar por frases como "as baterias são boas", "celular é bom", "a câmera é excelente", etc.
   

- **Ordenar documentos:**  
  Para listar os reviews ordenados pela nota (rating), do maior para o menor:
  ```
  GET erbd-reviews-index/_search
  {
    "sort": [
      { "rating": "desc" }
    ]
  }
  ```

- **Exemplo de busca com curingas:**  
  Para buscar palavras que começam com "bat" (ex: bateria, baterias):
  ```
  GET erbd-reviews-index/_search
  {
    "query": {
      "query_string": {
        "query": "bat*"
      }
    }
  }
  ```

- **Exemplo usando operadores lógicos (AND, OR, NOT):**  
  Buscar reviews que contenham "bateria" e "excelente", ou "câmera", mas não "ruim":
  ```
  GET erbd-reviews-index/_search
  {
    "query": {
      "query_string": {
        "query": "(celular NOT ruim) AND (bateria AND excelente)"
      }
    }
  }
  ```

- **Exemplo de filtro numérico dentro do query_string:**  
  Buscar reviews com nota maior ou igual a 4:
  ```
  GET erbd-reviews-index/_search
  {
    "query": {
      "query_string": {
        "query": "rating:>=4"
      }
    }
  }
  ```

  - **Combinando operadores lógicos e filtros numéricos:**
    Buscar reviews que contenham "bateria" e "excelente", com nota maior ou igual a 5:
    ```
    GET erbd-reviews-index/_search
    {
      "query": {
        "query_string": {
          "query": "(celular NOT ruim) AND (bateria AND excelente) AND (rating:>=5)"
        }
      }
    }
    ```

    - **Exemplo de busca com frases exatas:**
    Para buscar reviews que contenham a frase exata "bateria excelente":
    ```
    GET erbd-reviews-index/_search
    {
      "query": {
        "query_string": {
          "query": "\"celular é bom\""
        }
      }
    }
    ```
    Isso retornará apenas os reviews que contêm exatamente essa frase.

    - **Aggregações:**
    Para contar quantos reviews existem para cada nota (rating):
    ```
    GET erbd-reviews-index/_search
    {
      "size": 0,
      "aggs": {
        "ratings_count": {
          "terms": {
            "field": "rating"
          }
        }
      }
    }
    ```
    Isso retornará a contagem de reviews para cada nota, permitindo entender a distribuição das avaliações.

    Agora usando o `query_string`:
    ```
    GET erbd-reviews-index/_search
    {
      "size": 0,
      "query": {
        "query_string": {
          "query": "bat*"
        }
      },
      "aggs": {
        "ratings_count": {
          "terms": {
            "field": "rating"
          }
        }
      }
    }
    ```

Essas consultas mostram o poder do query_string para buscas flexíveis e avançadas no Elasticsearch!

Uma informação importante é que ElasticSearch indexa os textos com um método adaptado do TF-IDF (Term Frequency-Inverse Document Frequency), chamado BM25.
BM25 se baseia na frequência de termos (TF) e na frequência inversa de documentos (IDF), ajustando a relevância dos resultados com base no tamanho do documento e evitando que palavras muito comuns dominem os resultados.

- Links importantes:
  - [Documentação do Kibana](https://www.elastic.co/guide/en/kibana/current/index.html)
  - [Search API](https://www.elastic.co/guide/en/elasticsearch/reference/current/search.html)
  - [Query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)



## C. Ingerindo dados reais de reviews de produtos

No lugar onde obtemos criamos dados ficticios, vamos buscar os dados reais. Para isso vamos buscar dados da loja de aplicativos do Google Play, especificamente os dados de reviews de aplicativos. Para isso, utilizaremos a biblioteca `google_play_scraper` para coletar os dados.

```python
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
for result in result_list:
    review = {
        "id": result['reviewId'],
        "text": result['content'],
        "rating": result['score']
    }
    logger.info(f"Review: {review}")
    reviews.append(review)
```

Basta copiar este código na linha em que temos `reviews = []` e rodar o script novamente. Isso irá buscar os dados reais de reviews do aplicativo da Caixa Econômica Federal.

Temos uma interface web para visualizar os resultados das buscas:
```bash
python app_search.py
```
Acesse a interface em: [http://localhost:8000](http://localhost:8000)

## D. Buscas Semânticas com Embeddings

Agora, alem de indexar os textos dos reviews, vamos gerar embeddings para cada sentença dos reviews usando a biblioteca `sentence-transformers`. O objetivo é permitir buscas semânticas, onde a consulta é transformada em vetor e comparada com os vetores dos reviews.

No arquivo `script_embeddings.py`, inicialmente, os reviews são coletados, mas não há geração de embeddings nem divisão em sentenças. Para implementar a busca semântica, siga os passos abaixo (como feito em `script_embeddings_solved.py`):

```python
reviews = []
for result in result_list:
    content = result['content'].strip()    
    for i, sentence in enumerate(content.split('.')):
        if len(sentence.strip()) < 20:
            continue
        
        review = {
            "id_review": result['reviewId'],
            "id": f"`{result['reviewId']}#{i}",
            "text": result['content'],
            "rating": result['score'],
            "sentence": sentence.strip()
        }
        logger.info(f"Review: {review}")
        reviews.append(review)

from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('intfloat/multilingual-e5-small')

for review in tqdm(reviews):
    # encode the text to get its vector representation
    review['sentence_embeddings'] = model.encode(review['sentence'], convert_to_tensor=True).tolist() 
```

Basta copiar este código na linha em que temos `reviews = []` e rodar o script novamente. Isso irá buscar os dados reais de reviews do aplicativo da Caixa Econômica Federal.

Além disso, onde temos `query_vector = []``, vamos gerar o vetor da consulta:

```python
query_vector = model.encode(query, convert_to_tensor=True).tolist()
```

Dessa forma, a busca semântica permite encontrar reviews relevantes mesmo quando a consulta não contém exatamente as mesmas palavras dos textos indexados, superando as limitações da busca textual tradicional.

## E. Buscas Semânticas com Embeddings

RFF (Reciprocal rank fusion) é uma técnica de fusão de rankings que combina resultados de diferentes sistemas de busca, atribuindo pontuações a cada resultado com base na posição em que aparecem nos rankings individuais. Essa abordagem é útil para melhorar a precisão e a relevância dos resultados finais, aproveitando as forças de cada sistema.

Neste link você encontra o material de como fazer a fusão de rankings com RRF com ElasticSearch: [RRF](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion.html)


## Autores

* **Carlos Andres Ferrero** - [GitHub](https://github.com/anfer86) - Linkedin: [Carlos Andres Ferrero](https://www.linkedin.com/in/carlos-andres-ferrero/)

## Afiliação

* **Instituto Federal de Santa Catarina (IFSC)**
* **Centro de Excelência em Inteligência Artificial (CEIA) - UFG** (https://ceia.ufg.br/) (https://www.linkedin.com/company/centrodeexcelenciaemia/)
* **Birdie** (https://www.birdie.ai/) (https://www.linkedin.com/company/usebirdie/)

