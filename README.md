# ElasticSearch na Prática: Busca Textual e Semântica com Embeddings

Este repositório contém os materiais da oficina **"ElasticSearch na prática: Busca Textual e Semântica com Embeddings"**, apresentada na **Escola Regional de Banco de Dados (ERBD) 2025**.

## Descrição

Nesta oficina, exploraremos como estruturar buscas eficientes utilizando ElasticSearch, desde consultas textuais tradicionais até buscas semânticas com embeddings. Vamos instanciar localmente um ambiente com ElasticSearch e Kibana via Docker, criar um índice e indexar dados reais de reviews usando Python. A partir disso, compararemos buscas sintáticas e semânticas, demonstrando como embeddings podem aprimorar a relevância dos resultados.

Essa é uma oportunidade prática para entender e aplicar técnicas modernas de busca de informação em grandes conjuntos de dados textuais, e como integrar essas técnicas em processos de **Retrieval-Augmented Generation (RAG)**, essencial para melhorar as respostas geradas pelos atuais modelos de linguagem.

## Requisitos

* Computador com possibilidade de rodar **Docker**
* IDE para ElasticSearch (ex.: Kibana, Postman, DevTools do Chrome)
* **Python** instalado para execução de scripts
* Editor de texto ou IDE (ex.: VSCode, PyCharm)

## Instalação e Configuração

### 1. Clonar este repositório
```bash
$ git clone https://github.com/seu-usuario/elastic-search-erbd-2025.git
$ cd elastic-search-erbd-2025
```

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

## Executando Scripts de Indexação

Para rodar o primeiro script de indexação, execute:
```bash
$ python script_test.py
```

## Entendendo o Script de Teste:

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

- **Ordenar documentos:**  
  Para listar os reviews ordenados pela nota (rating), do maior para o menor:
  ```
  GET erbd-reviews-index/_search
  {
    "query": {
      "query_string": {
        "query": "*"
      }
    },
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

## Conteúdo do Curso

1. Ingestão de Dados:

A partir do `script_test.py`, vamos realizar uma cópia do arquivo e renomear o arquivo para `script_1.py`.

No lugar onde obtemos criamos dados ficticios, vamos buscar os dados reais. Para isso vamos buscar dados da loja de aplicativos do Google Play, especificamente os dados de reviews de aplicativos. Para isso, utilizaremos a biblioteca `google_play_scraper` para coletar os dados.

```python
from google_play_scraper import reviews, Sort

app_id = 'br.com.gabba.Caixa' # ID do aplicativo
result, continuation_token = reviews(
    app_id,
    lang='pt',
    country='br',
    sort=Sort.MOST_RELEVANT,
    count=5
)

reviews = []
for review in result:
    reviews.append({
        "id": review['reviewId'],
        "text": review['content'],
        "rating": review['score']
    })
```

## Autores

* **Carlos Andres Ferrero** - [GitHub](https://github.com/anfer86)

## Afiliação

* **Instituto Federal de Santa Catarina (IFSC)**
* **Centro de Excelência em Inteligência Artificial (CEIA) - UFG**
* **Birdie**

