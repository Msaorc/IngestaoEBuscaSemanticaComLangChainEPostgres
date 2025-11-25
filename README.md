# Desafio Ingestão e Busca Dinâmica com LangChain

Este projeto demonstra um pipeline de ingestão e busca de documentos usando LangChain, Google Generative AI, e PGVector. O sistema permite que um usuário faça perguntas sobre um documento PDF e obtenha respostas geradas por um modelo de linguagem.

## Funcionalidades

-   **Ingestão de Documentos**: Processa um arquivo PDF, divide-o em partes, gera embeddings e os armazena em um banco de dados vetorial (PGVector).
-   **Busca Semântica**: Utiliza um retriever para buscar partes relevantes do documento com base na pergunta do usuário.
-   **Geração de Respostas**: Usa um modelo de linguagem da Google (Gemini) para gerar respostas com base no contexto recuperado.
-   **Chat Interativo**: Permite que o usuário interaja com o sistema através de um terminal.

## Pré-requisitos

-   Docker e Docker Compose
-   Python 3.9 ou superior
-   Conta na Google AI Studio com uma chave de API

## Configuração do Ambiente

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

2.  **Crie e configure o arquivo de ambiente:**

    Copie o arquivo `.env.example` para `.env`:

    ```bash
    cp .env.example .env
    ```

    Abra o arquivo `.env` e preencha as variáveis de ambiente:

    -   `GOOGLE_API_KEY`: Sua chave de API do Google AI Studio.
    -   `GOOGLE_EMBEDDING_MODEL`: O modelo de embedding a ser usado (ex: `models/embedding-001`).
    -   `PGVECTOR_URL`: A URL de conexão com o banco de dados PostgreSQL.
    -   `PGVECTOR_COLLECTION_NAME`: O nome da coleção no PGVector.
    -   `PDF_PATH`: O caminho para o diretório que contém o `document.pdf`.

3.  **Instale as dependências:**

    Crie um ambiente virtual e instale as dependências do Python:

    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

4.  **Coloque o documento PDF:**

    Certifique-se de que o arquivo `document.pdf` está presente na raiz do projeto.

## Execução

1.  **Inicie o banco de dados:**

    Suba o container do PostgreSQL com o PGVector usando o Docker Compose:

    ```bash
    docker-compose up -d
    ```

2.  **Ingestão dos dados:**

    Execute o script de ingestão para processar o PDF e popular o banco de dados:

    ```bash
    python src/ingest.py
    ```

3.  **Inicie o chat:**

    Execute o script de chat para começar a fazer perguntas:

    ```bash
    python src/chat.py
    ```

    O terminal ficará aguardando suas perguntas. Para sair, digite `sair`.

## Estrutura do Projeto

```
.
├── docker-compose.yml
├── document.pdf
├── requirements.txt
├── .env.example
└── src
    ├── ingest.py
    ├── search.py
    └── chat.py
```

-   `docker-compose.yml`: Define o serviço do banco de dados PostgreSQL com a extensão PGVector.
-   `document.pdf`: O documento a ser processado.
-   `requirements.txt`: Lista as dependências do Python.
-   `.env.example`: Arquivo de exemplo para as variáveis de ambiente.
-   `src/ingest.py`: Script para ingestão do documento no banco de dados.
-   `src/search.py`: Módulo que define a lógica de busca e o RAG chain.
-   `src/chat.py`: Script para interação com o usuário via terminal.
