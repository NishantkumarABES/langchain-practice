import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub
load_dotenv()

if __name__ == '__main__':
    file_path = "C:/Users/QSS/Downloads/The Ultimate Python Handbook.pdf"

    # Load the PDF file
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    # Split the documents into smaller chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30)
    chunks = text_splitter.split_documents(documents)


    embeddings = OpenAIEmbeddings()

    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local("faiss_index_react")


    new_vector_store = FAISS.load_local(
        "faiss_index_react", embeddings,
        allow_dangerous_deserialization=True
    )


    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_doc_chain = create_stuff_documents_chain(
        OpenAI(), retrieval_qa_chat_prompt
    )
    retrieval_chian = create_retrieval_chain(
        retriever=new_vector_store.as_retriever(),
        combine_docs_chain=combine_doc_chain
    )

    result = retrieval_chian.invoke({"input": "What are the feautes of this language."})
    print(result)