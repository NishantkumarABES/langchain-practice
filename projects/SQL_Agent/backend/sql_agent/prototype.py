from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0)

# First Prompt Template: Determines if metadata is enough or a tool is needed
DECISION_PROMPT = """
You are an expert SQL assistant. Given the database metadata, determine:
- If the metadata is **sufficient**, return the optimized SQL query.
- If additional data is needed, return the **tool name** (ListTables, GetTableSchema, GetSampleData).

---
### **Database Metadata:**
{retrieved_metadata}

### **User Request:**
{user_input}

---
### **Your Response (SQL Query or Tool Name):**
"""

decision_prompt = PromptTemplate(
    input_variables=["retrieved_metadata", "user_input"], 
    template=DECISION_PROMPT
)


decision_chain = LLMChain(llm=llm, prompt=decision_prompt)

def first_llm_call(retrieved_metadata, user_input):
    """Determines if an SQL query can be generated directly or if a tool is required."""
    return decision_chain.run(retrieved_metadata=retrieved_metadata, user_input=user_input)


# Second Prompt: If tool data is needed, refine SQL query
REFINEMENT_PROMPT = """
You have received additional database details from a tool.
Use this new knowledge to finalize the optimized SQL query.

---
### **Database Metadata:**
{retrieved_metadata}

### **Additional Tool Data:**
{additional_info}

### **User Request:**
{user_input}

---
### **Final Optimized SQL Query:**
SQL:
"""

refinement_prompt = PromptTemplate(
    input_variables=["retrieved_metadata", "user_input", "additional_info"], 
    template=REFINEMENT_PROMPT
)

refinement_chain = LLMChain(llm=llm, prompt=refinement_prompt)

def second_llm_call(retrieved_metadata, user_input, additional_info):
    """Refines SQL query using additional tool data if required."""
    return refinement_chain.run(
        retrieved_metadata=retrieved_metadata, 
        user_input=user_input, 
        additional_info=additional_info
    )

import re

def parse_sql_output(output):
    """Ensures the output is a valid SQL query."""
    sql_pattern = re.compile(r"^\s*SELECT\s", re.IGNORECASE)
    if sql_pattern.match(output):
        return output.strip()
    else:
        raise ValueError("Invalid SQL query generated")


def execute_pipeline(retrieved_metadata, user_input):
    """Executes the complete SQL generation pipeline."""
    
    # Step 1: First LLM Call
    first_output = first_llm_call(retrieved_metadata, user_input)

    # Step 2: Decision Handling
    if first_output.strip().upper().startswith("SELECT"):
        final_query = first_output  # Directly return SQL
    else:
        tool_to_use = first_output.strip()
        print(f"⚡ Using Tool: {tool_to_use}")

        # Step 3: Fetch additional data using the tool
        additional_info = call_database_tool(tool_to_use)

        # Step 4: Second LLM Call (Refinement)
        final_query = second_llm_call(retrieved_metadata, user_input, additional_info)

    # Step 5: Output Parsing
    return parse_sql_output(final_query)
