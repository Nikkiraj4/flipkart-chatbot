# Flipkart AI Chatbot
**A RAG-Powered Shopping Assistant for Product Discovery**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1.3-1C3C3C?logo=flask&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1.2.15-1C3C3C?logo=langchain&logoColor=white)
![AstraDB](https://img.shields.io/badge/AstraDB-Vector_Store-7B2FF7)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-F54E00)
![License: ISC](https://img.shields.io/badge/License-ISC-blue)

[GitHub →](https://github.com/Nikkiraj4/flipkart-chatbot)  |  [Architecture →](#technical-architecture)  |  [API Routes →](#api-routes)  |  [Local Setup →](#local-development)

---

## The Problem

Online shoppers browsing large e-commerce platforms like Flipkart face a common frustration — keyword search returns hundreds of irrelevant results, and there is no conversational way to:

- Ask natural language questions like *"suggest a good laptop under ₹50,000"*
- Get product recommendations from a real product database — not hallucinated responses
- See source products with actual names, categories, and prices behind every answer
- Get contextually aware replies that know when a greeting is just a greeting

The result: poor discovery experience, decision fatigue, and missed purchases.

---

## The Solution

Flipkart AI Chatbot is a Retrieval-Augmented Generation (RAG) pipeline built on top of a real Flipkart product dataset. It retrieves semantically relevant products from AstraDB vector store, feeds them as grounded context to LLaMA 3.3 70B via Groq, and returns accurate, source-backed answers — never making up products or prices.

```
User Query
      ↓
Flask API          /chat endpoint receives user message
      ↓
Greeting Check     detects greetings → skips retrieval, responds naturally
      ↓
AstraDB Retriever  semantic vector search → top 3 matching products
      ↓
Context Builder    formats retrieved docs into structured context string
      ↓
Groq LLM           LLaMA 3.3 70B streams response grounded in context
      ↓
Response           answer + source products (name, category, price)
      ↓
Flask Template     rendered chat UI served via index.html
```

---

## Key Features

| Feature | Capability |
|---|---|
| RAG Pipeline | Retrieves top 3 semantically matching products from AstraDB before generating any response |
| LLaMA 3.3 70B | Groq-hosted LLaMA 3.3 70B Versatile — fast, accurate, grounded responses |
| Streaming Response | LLM output streamed chunk-by-chunk for real-time feel |
| Grounded Answers | LLM uses ONLY retrieved product context — never invents products or prices |
| Greeting Detection | Detects casual greetings and responds naturally without triggering retrieval |
| Source Attribution | Every product answer includes source metadata — name, category, price |
| 10 Product Categories | Mobiles, Laptops, Headphones, Televisions, Tablets, Cameras, Women's Clothing, Men's Clothing, Home Appliances, Home Decor |
| Out-of-scope Handling | Politely redirects users to available categories when query has no matching products |
| Flask REST API | Clean `/chat` POST endpoint — easy to integrate with any frontend |
| CORS Enabled | Frontend and backend can run on separate origins |

---

## MVP Workflow

```
┌────────────────────────────────────────────────────────────┐
│  USER                                                       │
│  → Opens chat UI                                           │
│  → Types: "suggest a good headphone under ₹2000"          │
│  → Hits Send                                               │
└────────────────────┬───────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────┐
│  FLASK: POST /chat                                         │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ 1. Greeting Check                                   │  │
│  │    Not a greeting → proceed to retrieval            │  │
│  └──────────────────────┬──────────────────────────────┘  │
│                         │                                  │
│  ┌──────────────────────▼──────────────────────────────┐  │
│  │ 2. AstraDB Vector Retriever                         │  │
│  │    Semantic search → top 3 matching products        │  │
│  │    Returns: product_name, category, price, details  │  │
│  └──────────────────────┬──────────────────────────────┘  │
│                         │                                  │
│  ┌──────────────────────▼──────────────────────────────┐  │
│  │ 3. Context Builder                                  │  │
│  │    Formats retrieved docs into context string       │  │
│  └──────────────────────┬──────────────────────────────┘  │
│                         │                                  │
│  ┌──────────────────────▼──────────────────────────────┐  │
│  │ 4. Groq LLM — LLaMA 3.3 70B                        │  │
│  │    Streams grounded answer using only context       │  │
│  │    Temperature: 0.7                                 │  │
│  └──────────────────────┬──────────────────────────────┘  │
└───────────────────────────────────────────────────────────-┘
                     │
                     ▼
         JSON Response:
         {
           "answer": "Here are some headphones...",
           "sources": [
             { "name": "...", "category": "Headphones", "price": "₹1,799" }
           ]
         }
```

---

## How to Use the Chatbot

**Step 1 — Ask naturally**
Type any shopping query in plain English — *"best mobile under ₹15,000"*, *"suggest a laptop for coding"*, *"show me women's kurtas"*.

**Step 2 — Get grounded answers**
The chatbot retrieves real products from the database and answers using only that data. No hallucinations.

**Step 3 — Check sources**
Every response includes source cards showing the product name, category, and price that the answer was based on.

**Step 4 — Out of scope?**
If your query doesn't match any available category, the chatbot politely tells you which categories are available instead of making something up.

---

## Technical Architecture

```
flipkart-chatbot/
├── app.py                    # Flask entry point — routes, RAG chain, LLM config
├── requirements.txt          # All Python dependencies (pinned versions)
├── .env                      # Environment variables (not committed)
│
├── templates/
│   └── index.html            # Chat UI served by Flask
│
└── static/                   # CSS and JS assets for the chat frontend
```

---

## API Routes

| Method | Route | Description |
|---|---|---|
| GET | `/` | Serves the chat UI (index.html) |
| POST | `/chat` | Accepts `{ "message": "..." }` → returns `{ "answer": "...", "sources": [...] }` |

**Request format:**
```json
{
  "message": "suggest a good laptop under 50000"
}
```

**Response format:**
```json
{
  "answer": "Here are some laptops available...",
  "sources": [
    {
      "name": "Lenovo IdeaPad Slim 3",
      "category": "Laptops",
      "price": "₹45,990"
    }
  ]
}
```

---

## Local Development

### Prerequisites
- Python 3.10+
- AstraDB account (free tier works) with a `products` vector collection
- Groq API key (free tier works)

### Setup

```bash
# Clone the repository
git clone https://github.com/Nikkiraj4/flipkart-chatbot.git
cd flipkart-chatbot

# Install dependencies
pip install -r requirements.txt

# Create environment variables file
touch .env
```

Add the following to your `.env` file:

```env
ASTRA_DB_APPLICATION_TOKEN=your_astradb_token
ASTRA_DB_API_ENDPOINT=your_astradb_endpoint
GROQ_API_KEY=your_groq_api_key
```

```bash
# Start the server
python app.py
# → http://127.0.0.1:5000
```

---

## Technology Stack

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.10+ | Runtime |
| Flask | 3.1.3 | Web framework and REST API |
| flask-cors | 6.0.2 | Cross-origin request handling |
| LangChain | 1.2.15 | RAG chain orchestration |
| langchain-astradb | 1.0.0 | AstraDB vector store integration |
| langchain-groq | 1.1.2 | Groq LLM integration |
| AstraDB | — | Vector database for semantic product search |
| Groq + LLaMA 3.3 70B | — | LLM for grounded response generation |
| python-dotenv | 1.2.2 | Environment variable management |
| Streamlit | 1.56.0 | Optional UI layer |

---

## Future Scope

The following capabilities are planned for future development:

- **Cart Integration** — Add products to cart directly from chat response
- **Price Filter** — Natural language budget constraints mapped to vector search filters
- **Multi-turn Memory** — Conversation history so follow-up questions are context-aware
- **Product Images** — Display product images alongside source cards
- **Voice Input** — Speech-to-text for hands-free product discovery
- **Personalisation** — User preference tracking for better recommendations over time
- **Deployment** — Hosted public demo on Render or Railway

---

## Author

| Name | Role |
|---|---|
| Nikita Kumari | Full-Stack AI Developer |

Built with ❤️ using Python, LangChain, AstraDB & Groq  ·  Live at http://flipkart-chatbot-ndpj9netrkgvnt8avj6wej.streamlit.app ·  
