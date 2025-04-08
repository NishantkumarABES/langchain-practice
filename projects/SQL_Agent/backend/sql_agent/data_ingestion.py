import os
from langchain_text_splitters import CharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings

def ingest_metadata(metadata, database_name):
    """
    Ingest metadata from a specific database into Pinecone.
    Each chunk will include a database identifier.
    """
    # Add database identifier to metadata before splitting
    formatted_metadata = f"Database: {database_name}\n{metadata}"  

    # Split the documents into smaller chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30)
    chunks = text_splitter.split_text(formatted_metadata)  
    
    # Embed the chunks using OpenAI's embeddings
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    # Store embeddings in Pinecone
    vector_store = PineconeVectorStore(
        chunks,
        embeddings,
        pinecone_api_key=os.getenv("PINECONE_API_KEY"),
        index_name=os.environ['INDEX_NAME'],
        metadata=[{"database": database_name}] * len(chunks)  
    )

    return vector_store


if __name__ == "__main__":
    vector_store = ingest_metadata(metadata, database_name)
    query = "Retrieve table schema for users"
    retrieved_docs = vector_store.similarity_search(query, filter={"database": "my_database_1"})