# 🛒 Flipkart AI Assistant — RAG Chatbot

A production-grade **Retrieval-Augmented Generation (RAG)** chatbot built for a Flipkart product dataset. Ask questions about products, compare prices, and get AI-powered recommendations — all backed by a cloud vector database.

🔗 **Live Demo:** [flipkart-chatbot-ndpj9netrkgvnt8avj6wej.streamlit.app](https://flipkart-chatbot-ndpj9netrkgvnt8avj6wej.streamlit.app/)

---

## 🚀 Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq — LLaMA 3.3-70b-versatile |
| Vector Database | AstraDB (1024 dimensions, cosine similarity) |
| Embeddings | NVIDIA NV-Embed-QA via AstraDB Vectorize |
| Orchestration | LangChain (LCEL pipeline) |
| Web App | Streamlit |
| Backend API | Flask + REST |
| Language | Python 3.14 |

---

## 🧠 How It Works (RAG Architecture)

```
User Question
      ↓
Embed question using NVIDIA NV-Embed-QA
      ↓
Search AstraDB for top-3 similar products
      ↓
Inject retrieved products into LLM prompt
      ↓
Groq LLaMA 3.3 generates the answer
      ↓
Display answer + source product cards
```

---

## 📦 Project Structure

```
flipkart-rag-chatbot/
├── app.py                  ← Flask REST API backend
├── streamlit_app.py        ← Streamlit web interface
├── create_data.py          ← Generates product CSV dataset
├── ingest_data.py          ← Ingests data into AstraDB
├── flipkart_products.csv   ← Product dataset (37 products, 9 categories)
├── test_search.py          ← Vector search test
├── requirements.txt
└── .gitignore
```

---

## 🗂️ Dataset

37 products across 9 categories:

- 📱 Mobiles
- 💻 Laptops
- 🎧 Headphones
- 📺 Televisions
- 📱 Tablets
- 📷 Cameras
- 👗 Women's Clothing
- 👔 Men's Clothing
- 🏠 Home Appliances

---


## 💬 Example Questions

```
What is the price of iPhone 15?
Compare Samsung Galaxy S24 Ultra vs iPhone 15
Which headphones are best for noise cancellation?
Show me laptops under ₹60,000
What are the best budget products?
Suggest a good 4K TV
Trendy dresses for women
```

---

## 🔑 Environment Variables

| Variable | Description |
|---|---|
| `ASTRA_DB_APPLICATION_TOKEN` | AstraDB application token |
| `ASTRA_DB_API_ENDPOINT` | AstraDB API endpoint URL |
| `GROQ_API_KEY` | Groq API key for LLaMA access |

---

## 📸 Screenshots

> Flipkart AI Assistant — Live Chat Interface

[Flipkart AI Assistant]<img width="1075" height="658" alt="Screenshot 2026-04-04 at 10 36 53 PM" src="https://github.com/user-attachments/assets/9c2e497e-d5ac-4963-90c8-193ff7b2cff7" />


---

## 🛠️ Built With

- [LangChain](https://langchain.com/) — LLM orchestration
- [AstraDB](https://www.datastax.com/products/datastax-astra) — Vector database
- [Groq](https://groq.com/) — Ultra-fast LLM inference
- [Streamlit](https://streamlit.io/) — Web interface
- [Flask](https://flask.palletsprojects.com/) — REST API

---

## 👨‍💻 Author

**Nikita raj**
- GitHub: [@Nikkiraj4](https://github.com/Nikkiraj4)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
