from dotenv import load_dotenv

load_dotenv()

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

embeddings = OpenAIEmbeddings(model = "text-embedding-3-small")

def ingest_docs():
    docs_path = "langchain-docs/api.python.langchain.com/en/latest"
    loader = ReadTheDocsLoader(docs_path)
    raw_documents = loader.load

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=50,
    )

    documents = text_splitter.split_documents(raw_documents)

    for each_document in documents:
        new_url = each_document.metadata["source"]
        new_url = new_url.replace("langchain-docs", "https:/")
        each_document.metadata["source"] = new_url
    
    PineconeVectorStore.from_documents(
        documents, embeddings, 
        index_name = "langchain-docs-index"
    )


def ingest_docs2() -> None:
    



if __name__ == "__main__":
    ingest_docs()