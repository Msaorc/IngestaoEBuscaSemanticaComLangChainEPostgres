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
        retriever = store.as_retriever()

        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

        template = """
            Você é um assistente de resposta a perguntas.
            Responda a pergunta do usuário com base no seguinte contexto.
            Se o contexto não contiver a resposta, responda exatamente: "Não tenho informações necessárias para responder sua pergunta.".
            Não tente inventar uma resposta.

            Contexto:
            {context}

            Pergunta:
            {question}

            Resposta:
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
