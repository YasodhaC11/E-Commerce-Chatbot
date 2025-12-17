# AI-Powered E-Commerce Chatbot
An intelligent customer support chatbot for e-commerce platforms that handles both general policy questions and dynamic product searches using Generative AI.

This chatbot currently supports two intents:

-**faq**: Triggered when users ask questions related to the platform's policies or general information. eg. Is online payment available?

-**sql**: Activated when users request product listings or information based on real-time database queries. eg. Show me all nike shoes below Rs. 3000.

![Chatbot Demo](https://github.com/YasodhaC11/E-Commerce-Chatbot/blob/main/app/resources/product-ss.png))

## Architecture

![Chatbot Demo](https://github.com/YasodhaC11/E-Commerce-Chatbot/blob/main/app/resources/product-ss.png))

## 🚀 Features
-**Intelligent Query Routing** – Uses semantic-router with sentence-transformers/all-MiniLM-L6-v2 to classify user queries into FAQ or product search intents.

-**FAQ Handling with RAG** – Retrieval-Augmented Generation pipeline using ChromaDB vector database and Sentence Transformers embeddings to provide accurate answers from company FAQs.

-**Live Product Search (Text-to-SQL)** – Converts natural language product queries into complex SQLite queries using Groq Llama 3.3 70B Versatile model, retrieving real-time product details (brand, price, discount, rating).

-**Interactive UI** – Multi-turn conversational interface built with Streamlit.

-**Production-Ready Design** – Clean separation of concerns, environment variable management, and fast embedding-based routing.

## Tech Stack
Python 

Groq API (Llama 3.3 70B Versatile)

ChromaDB – Vector database for FAQ storage

Sentence Transformers – all-MiniLM-L6-v2 for embeddings and semantic routing

semantic-router – Intent classification

Streamlit – Frontend chat interface

SQLite – Product catalog database

python-dotenv – Environment management

## Folder Strucure
```
e-commerce-chatbot/
├── app/
│   ├── main.py              # Streamlit app entry point
│   ├── faq.py               # RAG pipeline (ChromaDB + Groq)
│   ├── sql_chain.py         # Text-to-SQL chain
│   └── router.py            # Semantic router logic
├── resources/
│   └── faq_data.csv         # FAQ questions and answers
├── db.sqlite                # Product database
├── .env                     # Environment variables (not committed)
├── requirements.txt
├── runtime.txt              # Python version for deployment
└── README.md
```

## Installation
1. Clone the repository:  
2. pip install -r requirements.txt
3. Inside app folder, create a .env file with your GROQ credentials as follows:
4. ```
   GROQ_MODEL=<Add the model name, e.g. llama-3.3-70b-versatile>
   GROQ_API_KEY=<Add your groq api key here>
   ```
5. Run the streamlit app by running the following command.
```streamlit run app/main.py```
