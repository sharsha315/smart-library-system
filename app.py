import os
from dotenv import load_dotenv
import streamlit as st
import sqlite3
from datetime import datetime, timedelta
from database import create_connection, initialize_database
from sql_agent import create_safe_agent, sanitize_query
from langchain_groq import ChatGroq

# --- Load environment variables from .env file ---
load_dotenv()

# --- Initializing GROQ API KEY ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# --- Configuration ---
st.set_page_config(page_title="Smart Library", layout="wide")

# --- Database Functions ---
def get_books(search=None):
    conn = create_connection()
    cur = conn.cursor()
    if search:
        cur.execute('''SELECT * FROM books 
                    WHERE title LIKE ? OR author LIKE ? OR genre LIKE ?''',
                    (f'%{search}%', f'%{search}%', f'%{search}%'))
    else:
        cur.execute("SELECT * FROM books")
    return cur.fetchall()

def borrow_book(book_id, name):
    due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
    conn = create_connection()
    with conn:
        conn.execute('''INSERT INTO borrowed (book_id, borrower_name, due_date)
                     VALUES (?, ?, ?)''', (book_id, name, due_date))
        conn.execute("UPDATE books SET stock = stock - 1 WHERE id = ?", (book_id,))
        conn.commit()

# --- AI Functions ---
def get_recommendation(query):
    try:
        # Get current inventory
        books = get_books()
        if not books:
            return "Our library is currently empty. Please check back later!"
            
        # Format book list for AI
        book_list = "\n".join([f"- {b[1]} by {b[2]} ({b[3]})" for b in books])
        
        llm = ChatGroq(
            temperature=0.7,
            api_key=GROQ_API_KEY,
            model_name="llama3-70b-8192"
        )
        
        prompt = f"""You are a helpful librarian assistant. Recommend books ONLY from our current inventory:
        
        **Available Books:**
        {book_list}
        
        **User Request:** {query}
        
        **Rules:**
        1. Only suggest books that match the user's request
        2. If no matches exist, suggest similar genres
        3. Never invent books not in our inventory
        4. Mention specific titles and authors
        5. Keep response under 3 sentences"""
        
        return llm.invoke(prompt).content
        
    except Exception as e:
        return f"Recommendation service unavailable. Error: {str(e)}"

    # llm = ChatGroq(
    #     temperature=0.7,
    #     api_key=GROQ_API_KEY,
    #     model_name="llama3-70b-8192"
    # )
    
    # prompt = f"""You're a friendly librarian. Recommend books from our collection:
    # Available books: 
    # - The Great Gatsby (Classic)
    # - 1984 (Dystopian)
    # - The Hobbit (Fantasy)
    # User request: {query}
    # Respond in 2 short, enthusiastic sentences."""
    
    # return llm.invoke(prompt).content

# --- Streamlit UI ---
def main():
    st.title("📚 Smart Library System")
    
    # Admin Auth
    admin_mode = st.sidebar.text_input("Admin Password:", type="password") == "admin123"
    
    # Initialize Agent
    sql_agent = create_safe_agent()
    
    # Tabs
    tabs = st.tabs(["Browse", "Borrow", "AI Assistant", "Help Desk"])
    
    with tabs[0]:  # Browse
        st.header("Book Inventory")
        search = st.text_input("Search books by title/author/genre:")
        for book in get_books(search):
            cols = st.columns([4,1])
            cols[0].subheader(f"{book[1]} by {book[2]}")
            cols[0].caption(f"Genre: {book[3]} | Stock: {book[5]}")
            if admin_mode and cols[1].button("❌ Delete", key=f"del{book[0]}"):
                conn = create_connection()
                conn.execute("DELETE FROM books WHERE id = ?", (book[0],))
                conn.commit()
                st.rerun()
        
        if admin_mode:
            # In the "Add New Book" expander section:
            with st.expander("➕ Add New Book"):
                title = st.text_input("Title*")
                author = st.text_input("Author*")
                genre = st.text_input("Genre*")
                isbn = st.text_input("ISBN* (13-digit number)")
                stock = st.number_input("Initial Stock*", min_value=1, value=1)
                
                if st.button("Add Book"):
                    # Validate required fields
                    if not all([title, author, genre, isbn]):
                        st.error("Please fill all required fields (*)")
                    else:
                        conn = create_connection()
                        cursor = conn.cursor()
                        
                        # Check for existing ISBN
                        cursor.execute("SELECT id FROM books WHERE isbn = ?", (isbn,))
                        if cursor.fetchone():
                            st.error("ISBN already exists! Each book must have a unique ISBN.")
                        else:
                            conn.execute('''INSERT INTO books 
                                        (title, author, genre, isbn, stock)
                                        VALUES (?, ?, ?, ?, ?)''',
                                        (title, author, genre, isbn, stock))
                            conn.commit()
                            st.success(f"Added {title} to inventory!")
                            st.rerun()

    
    with tabs[1]:  # Borrow
        st.header("Borrow a Book")
        name = st.text_input("Your Name")
        selected = st.selectbox("Choose Book", get_books())
        if st.button("Borrow"):
            borrow_book(selected[0], name)
            st.success(f"Borrowed {selected[1]}! Due: {(datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')}")
    
    with tabs[2]:  # AI Assistant
        st.header("Book Recommendation Engine")
        st.caption("Get personalized reading suggestions")  
        query = st.text_input("What kind of books are you looking for?")
        if query:
            response = get_recommendation(query)
            st.markdown(f"**🤖 AI Suggests:** {response}")
    
    with tabs[3]:  # NL Query
        st.header("Library Analytics")
        st.caption("Ask factual questions about inventory/borrowers \n Example: Show fantasy books with more than 2 copies")
        nl_query = st.text_input("Ask about books:")
        
        if nl_query:
            if not sanitize_query(nl_query):
                st.error("Query blocked for security reasons.")
            else:
                try:
                    result = sql_agent.run(nl_query)
                    st.markdown(f"**📊 Result:**\n{result}")
                except Exception as e:
                    st.error(f"AI failed to process query: {str(e)}")

if __name__ == "__main__":
    initialize_database()
    main()