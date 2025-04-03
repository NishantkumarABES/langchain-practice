import os

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_pinecone import PineconeVectorStore
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables import RunnablePassthrough
from langchain import hub

def format_doc(docs):
    return "\n\n".join([doc.page_content for doc in docs])


if __name__ ==  "__main__":
    embeddings = OpenAIEmbeddings()
    llm = ChatOpenAI()

    vector_store = PineconeVectorStore(
        index = os.environ['INDEX_NAME'],
        embedding = embeddings
    )

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_doc_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
    retrieval_chian = create_retrieval_chain(
        retriever=vector_store.as_retriever(),
        combine_docs_chain=combine_doc_chain
    )

    query = "What is vector store in machine learning"
    result = retrieval_chian.invoke({"input": query})
    print(result)

    template = """
    Use the following pieces of context to answer at the end. If you don't know the answer, 
    just say that you don't know, don't try to make up an answer. use three sentences maximum
    and keep the answer as consise as possible.
    Always say "thankyou for asking!" at the end of answer

    {context}

    Question: {question}

    helpful answer:
    """

    custom_rag_prompt = PromptTemplate.from_template(template)

    rag_chain = (
        {
            "context": vector_store.as_retriever() | format_doc,  "question": RunnablePassthrough()
        } | custom_rag_prompt | llm 
    )

    result = rag_chain.invoke({"input": query})
    print(result)