import os
from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_pinecone import PineconeVectorStore

from agent_prompt import SQL_PROMPT_TEMPLATE_BASIC

# Load OpenAI model
llm = ChatOpenAI(model="gpt-4", temperature=0)

# 🔹 Prompt Template for SQL Query Generation
SQL_PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["retrieved_metadata", "user_input"],
    template=SQL_PROMPT_TEMPLATE_BASIC
)


embeddings = OpenAIEmbeddings()
vector_store = PineconeVectorStore(
    index = os.environ['INDEX_NAME'],
    embedding = embeddings
)

def format_doc(docs):
    return "\n\n".join([doc.page_content for doc in docs])


if __name__ == '__main__':
    print("Welcome to SQL Agent...")
    
    user_input = "Get all products with a price greater than $50."
    sql_chain = {
        "context": vector_store.as_retriever() | format_doc,  
        "question": RunnablePassthrough()
    } | SQL_PROMPT_TEMPLATE | llm  
    
    generated_query = sql_chain.invoke({"input": user_input})
    print(generated_query)