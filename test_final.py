import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# 1. This line looks for your .env file and reads the keys
load_dotenv()

# 2. This sets up the 'Brain' using your Groq Key
# We are using Llama 3, which is incredibly fast for RAG projects
try:
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile"
    )

    # 3. Sending the first message
    print("Connecting to Groq AI... Please wait.")
    response = llm.invoke("Hello! I am Nikita. We are setting up a Flipkart AI Chatbot. Is the connection working?")
    
    print("\n--- AI RESPONSE ---")
    print(response.content)
    print("-------------------\n")
    print("SUCCESS: Your Mac is now connected to the AI!")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\nTip: Make sure your .env file has the correct GROQ_API_KEY.")