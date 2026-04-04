import os
import streamlit as st
from dotenv import load_dotenv
from langchain_astradb import AstraDBVectorStore
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

# --- Page Config ---
st.set_page_config(
    page_title="Flipkart AI Assistant",
    page_icon="🛒",
    layout="centered"
)

# --- Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif; }

    .stApp {
        background: linear-gradient(135deg, #f0f4ff 0%, #f8f9ff 100%);
        min-height: 100vh;
    }

    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 0 !important; max-width: 780px; }

    /* ── HEADER ── */
    .fk-header {
        background: linear-gradient(135deg, #2874f0 0%, #1a5dc8 100%);
        border-radius: 0 0 24px 24px;
        padding: 20px 28px 20px;
        margin-bottom: 28px;
        box-shadow: 0 4px 20px rgba(40,116,240,0.3);
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .fk-logo { font-size: 38px; line-height: 1; }
    .fk-title { color: white; font-size: 22px; font-weight: 700; margin: 0; }
    .fk-badge {
        display: inline-block;
        background: rgba(255,255,255,0.18);
        color: #d6e8ff;
        font-size: 11px;
        font-weight: 500;
        padding: 3px 10px;
        border-radius: 20px;
        margin-top: 4px;
        border: 1px solid rgba(255,255,255,0.25);
    }

    /* ── USER BUBBLE ── */
    .user-row {
        display: flex;
        justify-content: flex-end;
        align-items: flex-end;
        gap: 8px;
        margin: 8px 0;
    }
    .user-bubble {
        background: linear-gradient(135deg, #2874f0, #1a5dc8);
        color: white;
        padding: 12px 18px;
        border-radius: 20px 20px 4px 20px;
        max-width: 70%;
        font-size: 14px;
        line-height: 1.5;
        box-shadow: 0 2px 12px rgba(40,116,240,0.35);
    }
    .user-avatar {
        width: 34px; height: 34px;
        background: #2874f0;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 16px;
        flex-shrink: 0;
    }

    /* ── BOT BUBBLE ── */
    .bot-row {
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
        gap: 8px;
        margin: 8px 0;
    }
    .bot-avatar {
        width: 34px; height: 34px;
        background: linear-gradient(135deg, #ff6d00, #ff9800);
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 16px;
        flex-shrink: 0;
        margin-top: 4px;
    }
    .bot-bubble {
        background: white;
        color: #1a1a2e;
        padding: 14px 18px;
        border-radius: 20px 20px 20px 4px;
        max-width: 75%;
        font-size: 14px;
        line-height: 1.6;
        box-shadow: 0 2px 16px rgba(0,0,0,0.08);
        border: 1px solid #eef2ff;
    }

    /* ── PRODUCT CARDS ── */
    .sources-label {
        font-size: 11px;
        font-weight: 600;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin: 10px 0 6px 42px;
    }
    .product-cards {
        display: flex;
        gap: 10px;
        margin-left: 42px;
        flex-wrap: wrap;
        margin-bottom: 12px;
    }
    .product-card {
        background: white;
        border: 1.5px solid #e8f0ff;
        border-radius: 14px;
        padding: 12px 14px;
        min-width: 160px;
        max-width: 180px;
        box-shadow: 0 2px 10px rgba(40,116,240,0.07);
        transition: transform 0.2s;
        cursor: default;
    }
    .product-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(40,116,240,0.13); }
    .pc-emoji { font-size: 22px; margin-bottom: 6px; }
    .pc-name { font-size: 12px; font-weight: 600; color: #1a1a2e; line-height: 1.3; margin-bottom: 4px; }
    .pc-cat { font-size: 11px; color: #888; margin-bottom: 6px; }
    .pc-price {
        font-size: 14px; font-weight: 700;
        color: #2874f0;
        background: #eef4ff;
        display: inline-block;
        padding: 2px 8px;
        border-radius: 8px;
    }

    /* ── WELCOME CARD ── */
    .welcome-card {
        background: white;
        border-radius: 20px;
        padding: 28px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        border: 1px solid #eef2ff;
        margin-bottom: 24px;
    }
    .welcome-card h3 { color: #1a1a2e; font-size: 18px; margin-bottom: 8px; }
    .welcome-card p { color: #666; font-size: 13px; margin-bottom: 16px; }
    .suggestion-chips { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; }
    .chip {
        background: #eef4ff;
        color: #2874f0;
        border: 1.5px solid #c8dcff;
        border-radius: 20px;
        padding: 6px 14px;
        font-size: 12px;
        font-weight: 500;
    }

    /* ── INPUT ── */
    .stTextInput > div > div > input {
        border: 2px solid #e8f0ff !important;
        background: #f5f7ff !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        color: #1a1a2e !important;
        box-shadow: none !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #2874f0 !important;
        background: #eef4ff !important;
        outline: none !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #2874f0, #1a5dc8) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 20px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        width: 100% !important;
        box-shadow: 0 4px 12px rgba(40,116,240,0.3) !important;
    }
    .stButton > button:hover {
        box-shadow: 0 6px 20px rgba(40,116,240,0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# ── HEADER ──
st.markdown("""
<div class="fk-header">
    <div class="fk-logo">🛒</div>
    <div>
        <div class="fk-title">Flipkart AI Assistant</div>
        <span class="fk-badge">🤖 AI-Powered Shopping</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── SESSION STATE ──
if "messages" not in st.session_state:
    st.session_state.messages = []
if "all_sources" not in st.session_state:
    st.session_state.all_sources = []

# ── LOAD CHAIN ──
@st.cache_resource
def load_chain():
    vstore = AstraDBVectorStore(
        collection_name="products",
        token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"),
        api_endpoint=os.getenv("ASTRA_DB_API_ENDPOINT"),
        autodetect_collection=True
    )
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile",
        temperature=0.7
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a helpful Flipkart shopping assistant. "
         "Use the context below to answer questions about products.\n\n"
         "Context: {context}"),
        ("human", "{input}"),
    ])
    retriever = vstore.as_retriever(search_kwargs={"k": 3})
    return llm, prompt, retriever

llm, prompt, retriever = load_chain()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_category_emoji(category):
    mapping = {
        "mobile": "📱", "smartphone": "📱",
        "laptop": "💻", "computer": "💻",
        "headphones": "🎧", "audio": "🎧",
        "tv": "📺", "television": "📺",
        "tablet": "📱",
    }
    for key, emoji in mapping.items():
        if key in category.lower():
            return emoji
    return "🛍️"

# ── WELCOME CARD ──
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-card">
        <h3>👋 How can I help you shop today?</h3>
        <p>Ask me anything about products, prices, comparisons, or recommendations.</p>
        <div class="suggestion-chips">
            <span class="chip">📱 Best smartphones?</span>
            <span class="chip">💻 Laptops under ₹90,000</span>
            <span class="chip">🎧 Which headphones?</span>
            <span class="chip">⚖️ Compare Samsung vs iPhone</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── CHAT HISTORY ──
source_idx = 0
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="user-row">
            <div class="user-bubble">{msg["content"]}</div>
            <div class="user-avatar">🧑</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="bot-row">
            <div class="bot-avatar">🤖</div>
            <div class="bot-bubble">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

        # Product source cards (only if docs exist)
        if source_idx < len(st.session_state.all_sources):
            docs = st.session_state.all_sources[source_idx]
            if docs:  # empty list for greetings = no cards
                cards_html = '<div class="sources-label">📦 Products Retrieved</div><div class="product-cards">'
                for doc in docs:
                    meta = doc.metadata
                    name  = meta.get("product_name", "Unknown")
                    cat   = meta.get("category", "Product")
                    price = meta.get("price", "N/A")
                    emoji = get_category_emoji(cat)
                    cards_html += f"""
                    <div class="product-card">
                        <div class="pc-emoji">{emoji}</div>
                        <div class="pc-name">{name}</div>
                        <div class="pc-cat">{cat}</div>
                        <div class="pc-price">₹{price}</div>
                    </div>"""
                cards_html += "</div>"
                st.markdown(cards_html, unsafe_allow_html=True)
            source_idx += 1

# ── INPUT AREA ──
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input(
        "msg",
        placeholder="e.g. Which laptop should I buy under ₹90,000?",
        label_visibility="collapsed",
        key="user_input"
    )
with col2:
    send = st.button("Send 🚀")

# ── HANDLE QUERY ──
GREETINGS = {"hi", "hello", "hey", "hlo", "hii", "sup", "yo",
             "good morning", "good evening", "good afternoon"}

if send and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})

    is_greeting = user_input.strip().lower() in GREETINGS

    if is_greeting:
        docs = []
        context_text = "No specific product context needed."
    else:
        docs = retriever.invoke(user_input)
        context_text = format_docs(docs)

    full_response = ""
    for chunk in (prompt | llm | StrOutputParser()).stream({
        "context": context_text,
        "input": user_input
    }):
        full_response += chunk

    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.session_state.all_sources.append(docs)
    st.rerun()