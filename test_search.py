import os
from dotenv import load_dotenv
from langchain_astradb import AstraDBVectorStore

# 1. Load your credentials
load_dotenv()

# 2. Connect to the 'products' collection you just filled
vstore = AstraDBVectorStore(
    collection_name="products",
    token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"),
    api_endpoint=os.getenv("ASTRA_DB_API_ENDPOINT"),
    autodetect_collection=True
)

# 3. Define a "Natural Language" query
# Note: We aren't just searching for keywords!
query = "I want a high-end phone with a great camera"

print(f"\n🔍 AI is searching for: '{query}'...")

# 4. Perform the search (k=2 means give us the top 2 matches)
results = vstore.similarity_search(query, k=2)

print("\n--- 🎯 TOP MATCHES FROM ASTRADB ---")
for i, doc in enumerate(results, 1):
    print(f"\nResult #{i}:")
    print(doc.page_content)
    print("-" * 30)