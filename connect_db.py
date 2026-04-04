import os
from dotenv import load_dotenv
from langchain_astradb import AstraDBVectorStore

load_dotenv()

# Get credentials from your .env
TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")

try:
    print("Connecting to AstraDB...")
    # This initializes the connection to your 'flipkart_db'
    vstore = AstraDBVectorStore(
        embedding=None, # We will add embeddings in the next step
        collection_name="products",
        token=TOKEN,
        api_endpoint=ENDPOINT,
    )
    print("✅ SUCCESS: Connected to AstraDB!")
    
except Exception as e:
    print(f"❌ Connection Failed: {e}")