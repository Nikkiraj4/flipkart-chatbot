import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from langchain_astradb import AstraDBVectorStore
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

app = Flask(__name__)
CORS(app)

# ── Load chain once at startup ──
print("🔌 Connecting to AstraDB...")
vstore = AstraDBVectorStore(
    collection_name="products",
    token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"),
    api_endpoint=os.getenv("ASTRA_DB_API_ENDPOINT"),
    autodetect_collection=True
)

print("🧠 Loading Groq LLM...")
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0.7
)

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful Flipkart shopping assistant. "
     "Use ONLY the context below to answer questions about products. "
     "If the context does not contain relevant products, politely say that "
     "this category is not available and suggest closest categories from: "
     "Mobiles, Laptops, Headphones, Televisions, Tablets, Cameras, "
     "Women's Clothing, Men's Clothing, Home Appliances, Home Decor. "
     "Never make up products or prices.\n\n"
     "Context: {context}"),
    ("human", "{input}"),
])

retriever = vstore.as_retriever(search_kwargs={"k": 3})

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

print("✅ Flipkart RAG Chatbot is ready!")

# ── Routes ──
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"error": "Empty message"}), 400

    GREETINGS = {"hi", "hello", "hey", "hlo", "hii", "sup", "yo",
                 "good morning", "good evening", "good afternoon"}

    is_greeting = user_input.lower() in GREETINGS

    if is_greeting:
        docs = []
        context_text = "No specific product context needed."
    else:
        docs = retriever.invoke(user_input)
        context_text = format_docs(docs)

    # Generate answer
    full_response = ""
    for chunk in (prompt | llm | StrOutputParser()).stream({
        "context": context_text,
        "input": user_input
    }):
        full_response += chunk

    # Build sources list
    sources = []
    for doc in docs:
        meta = doc.metadata
        sources.append({
            "name":     meta.get("product_name", "Unknown"),
            "category": meta.get("category", "N/A"),
            "price":    meta.get("price", "N/A"),
        })

    return jsonify({
        "answer": full_response,
        "sources": sources
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)