from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


def build_vectorstore(chunks, persist_dir="chroma_db"):
    embeddings = OpenAIEmbeddings()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir
    )

    vectorstore.persist()
    return vectorstore


def load_vectorstore(persist_dir="chroma_db"):
    embeddings = OpenAIEmbeddings()

    return Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings
    )
