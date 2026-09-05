from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS


def create_vector_store(text):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    documents = text_splitter.create_documents([text])

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    vector_store = FAISS.from_documents(
        documents,
        embeddings
    )

    return vector_store


def search_resume(vector_store, query, k=3):

    results = vector_store.similarity_search(
        query,
        k=k
    )

    return results