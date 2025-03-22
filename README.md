# Smart Library System 📚
**AI-Powered Library Management System with Natural Language Interaction**

## 🚀 Why Smart Library?
Traditional library systems require complex training and manual data entry. Smart Library revolutionizes this by:
- **AI-Powered Search**: Query inventory using natural language ("Show fantasy books with >2 copies")
- **Instant Recommendations**: Get personalized book suggestions via Groq's Llama3-70B
- **Zero Training Needed**: Intuitive interface for staff and patrons
- **Open Source**: Free to use and modify under MIT license

## 🚀 Video Demo
[Watch Demo](https://www.loom.com/share/45fd9e6e1d5d47349086cf76abdcedd4?sid=68c42d29-ff88-45c1-b2b1-011d0e5027a4)  
*(Shows AI recommendations, NL queries, and admin controls)*

## 🚀 Tech Stack
| Component       | Technologies Used                             |
|-----------------|-----------------------------------------------|
| **AI Engine**   | Groq API (Llama3-70B), LangChain              |
| **Backend**     | Python 3.11, SQLAlchemy                       |
| **Database**    | SQLite (Production-ready: PostgreSQL)         |
| **Frontend**    | Streamlit                                     |
| **Security**    | Query Sanitization, RBAC                      |

## 🚀 Key Innovations:
- **Groq LPU Inference**: 300ms response times for AI features
- **LangChain ReAct Agent**: Converts natural language to SQL queries
- **Streamlit UI**: Responsive web interface in pure Python

## ⚙️ How It Works
1. **Natural Language Processing**  
   - Users ask questions in plain English ("Find books by Tolkien")
   - LangChain agent converts queries to SQL
   - Results displayed in simple tables

2. **AI Recommendations**  
   - Llama3-70B analyzes user preferences
   - Suggests books from inventory using semantic matching

3. **Admin Workflows**  
   - Add/remove books with 1 click
   - Track borrow history and stock levels

## 💻 Installation
```bash
# 1. Clone repository
git clone https://github.com/sharsha315/smart-library-system.git
cd smart-library-system

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Get Groq API key (free)
#    - Create account at https://console.groq.com
#    - Create .env file with:
GROQ_API_KEY = "your_key_here"

# 5. Initialize database
python database.py

# 6. Launch app
streamlit run app.py
```

## 📖 Usage Guide
1. **Patrons**
   - Search books via text/natural language
   - Borrow books with name input
   - Get AI recommendations

2. **Staff**
   - Password: **`admin123`**
   - Add/remove books
   - View all borrow records

3. **Demo Credentials**
   - Sample books pre-loaded: The Great Gatsby, 1984, The Hobbit

## 📜 License
MIT License - See [LICENSE](https://github.com/sharsha315/smart-library-system/blob/main/LICENSE) for details

## 📞 Contact
- Discord: **sharsha315**
- X (Twitter): [@sharsha315](https://www.x.com/sharsha315)