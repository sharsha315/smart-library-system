import os
from dotenv import load_dotenv
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain_groq import ChatGroq
import streamlit as st

# --- Load environment variables from .env file ---
load_dotenv()

# --- Initializing GROQ API KEY ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def create_safe_agent():
    # Restrict access to books table only
    db = SQLDatabase.from_uri(
        "sqlite:///books.db",
        include_tables=['books'],
        sample_rows_in_table_info=2
    )
    
    # Using Groq's Llama3-70B
    llm = ChatGroq(
        temperature=0,
        api_key=GROQ_API_KEY,
        model_name="llama3-70b-8192"
    )
    
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    
    return create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        handle_parsing_errors=True
    )

def sanitize_query(query: str) -> bool:
    BLACKLIST = ["DROP", "DELETE", "INSERT", "UPDATE", "CREATE", "ALTER"]
    return not any(word in query.upper() for word in BLACKLIST)