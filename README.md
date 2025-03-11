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

### 2. Subir o ambiente com ElasticSearch e Kibana

Utilizaremos o Docker Compose para criar o ambiente de busca.
```bash
$ docker-compose up -d
```
Isso iniciará:
- **ElasticSearch** na porta `9200`
- **Kibana** na porta `5601`

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
$ python script1.py
```
(Substitua `script1.py` pelo nome correto do arquivo.)

## Autores

* **Carlos Andres Ferrero** - [GitHub](https://github.com/anfer86)

## Afiliação

* **Instituto Federal de Santa Catarina (IFSC)**
* **Centro de Excelência em Inteligência Artificial (CEIA) - UFG**
* **Birdie**

