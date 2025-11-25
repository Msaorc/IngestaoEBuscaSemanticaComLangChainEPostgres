import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores.pgvector import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv(override=True)

PDF_PATH = os.path.join(os.getenv("PDF_PATH", ""), "document.pdf")
docs = PyPDFLoader(str(PDF_PATH)).load()

if not docs:
    print(f"Erro: Nenhum documento carregado de {PDF_PATH}. Verifique o caminho ou o conteúdo do PDF.")
    exit()

def ingest_pdf(docs):
    splits = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150,
        add_start_index=False
    ).split_documents(docs)

    ids = [f"doc-{i}" for i in range(len(splits))]

    embeddings = GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL","models/embedding-001"))

    PGVector.from_documents(
        splits,
        embeddings,
        collection_name=os.getenv("PGVECTOR_COLLECTION_NAME"),
        connection_string=os.getenv("PGVECTOR_URL"),
        use_jsonb=True,
        ids=ids,
        pre_delete_collection=True
    )

    print("Documentos processados com sucesso.")

ingest_pdf(docs)