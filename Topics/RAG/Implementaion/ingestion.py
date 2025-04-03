import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore


load_dotenv()
if __name__ == '__main__':
    loader = TextLoader("blog.txt")
    document = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    chunks = text_splitter.split_documents(documents=document)

    embeddings = OpenAIEmbeddings()

    vector_store = PineconeVectorStore(
        chunks,
        embeddings,
        pinecone_api_key=os.getenv("PINECONE_API_KEY"),
        index_name=os.environ['INDEX_NAME']
    )