import os
import pandas as pd
from dotenv import load_dotenv
from langchain_astradb import AstraDBVectorStore
from langchain_core.documents import Document

load_dotenv()

# 1. Load CSV
df = pd.read_csv("flipkart_products.csv")

# 2. Build Documents with BOTH page_content AND metadata
documents = []
for _, row in df.iterrows():
    content = (
        f"Product: {row['product_name']}\n"
        f"Category: {row['category']}\n"
        f"Price: {row['price']}\n"
        f"Description: {row['description']}"
    )
    metadata = {
        "product_id":   str(row["product_id"]),
        "product_name": str(row["product_name"]),
        "category":     str(row["category"]),
        "price":        str(row["price"]),
    }
    documents.append(Document(page_content=content, metadata=metadata))

# 3. Connect to AstraDB
vstore = AstraDBVectorStore(
    collection_name="products",
    token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"),
    api_endpoint=os.getenv("ASTRA_DB_API_ENDPOINT"),
    autodetect_collection=True
)

# 4. Clear old documents and re-ingest
print("🗑️  Clearing old documents...")
vstore.clear()

print(f"⬆️  Ingesting {len(documents)} products with metadata...")
vstore.add_documents(documents)

print("✅ Re-ingestion complete! Metadata is now stored.")