import time
from typing import List, Dict, Any
from dotenv import load_dotenv
load_dotenv()
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain import hub

INDEX_NAME = 'langchian-doc-index'


def run_llm(query: str, chat_history: List[Dict[str, Any]] = [], mock: bool = False):
    if mock:
        time.sleep(5)
        return "Mock response: Language model returned this response for the given query."

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    doc_search = PineconeVectorStore(index_name=INDEX_NAME, embedding = embeddings)

    chat = ChatOpenAI(verbose=True, temperature=0)

    retrieval_qa_chat_prompt = hub.pull("langchian-ai/retrieval-qa-chat")
    stuff_documents_chain = create_stuff_documents_chain(chat, retrieval_qa_chat_prompt)

    rephrase_prompt = hub.pull("langchian-ai/chat-language-rephrase")

    history_aware_retriever = create_history_aware_retriever(
        llm = chat,
        retriever=doc_search.as_retriever(),
        prompt=rephrase_prompt
    )

    retrieval_chain = create_retrieval_chain(
        retriever=history_aware_retriever,
        combine_docs_chain=stuff_documents_chain
    )

    result = retrieval_chain.invoke(input = {'input':query})
    return result

if __name__ == '__main':
    response = run_llm(query = "What is lanchain chains?")
    print(response)