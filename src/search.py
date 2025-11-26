import os
from dotenv import load_dotenv
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

def search():
    """
    Initializes and returns a RAG chain for answering questions based on documents
    stored in a PGVector database.
    """
    try:
        load_dotenv(override=True)

        embeddings = GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL"))
        
        connection_string = os.getenv("PGVECTOR_URL")
        collection_name = os.getenv("PGVECTOR_COLLECTION_NAME")

        store = PGVector(
            connection_string=connection_string,
            collection_name=collection_name,
            embedding_function=embeddings,
        )
        retriever = store.as_retriever(search_kwargs={"k": 10})

        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
        
        template = """
        CONTEXTO:
        {context}

        REGRAS:
        - Responda somente com base no CONTEXTO.
        - Se a informação não estiver explicitamente no CONTEXTO, responda:
        "Não tenho informações necessárias para responder sua pergunta."
        - Nunca invente ou use conhecimento externo.
        - Nunca produza opiniões ou interpretações além do que está escrito.

        EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
        Pergunta: "Qual é a capital da França?"
        Resposta: "Não tenho informações necessárias para responder sua pergunta."

        Pergunta: "Quantos clientes temos em 2024?"
        Resposta: "Não tenho informações necessárias para responder sua pergunta."

        Pergunta: "Você acha isso bom ou ruim?"
        Resposta: "Não tenho informações necessárias para responder sua pergunta."

        PERGUNTA DO USUÁRIO:
        {question}

        RESPONDA A "PERGUNTA DO USUÁRIO"
        """

        prompt = ChatPromptTemplate.from_template(template)

        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        
        return rag_chain

    except Exception as e:
        print(f"Erro ao inicializar a busca: {e}")
        return None
