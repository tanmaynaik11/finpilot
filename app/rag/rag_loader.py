from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

def load_rag_db(persist_dir="chroma_db"):
    loader = TextLoader("data/context_docs.txt")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=20)
    chunks = splitter.split_documents(docs)

    embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma.from_documents(chunks, embedder, persist_directory=persist_dir)
    vectordb.persist()
    return vectordb
