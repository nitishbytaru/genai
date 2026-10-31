import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings,ChatGoogleGenerativeAI
from langchain_qdrant import QdrantVectorStore
from langchain_core.messages import SystemMessage, HumanMessage

import sys
import time

load_dotenv()

def type_text(text, delay=0.01):
    """Print text with a simple typing effect."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def print_header():
    print("\033[96m")
    print("╔" + "═" * 48 + "╗")
    print("║" + " 🤖  RAG ASSISTANT ".center(48) + "║")
    print("║" + " 📚 Your Personal PDF Knowledge Bot ".center(48) + "║")
    print("╚" + "═" * 48 + "╝")
    print("\033[0m")

def print_answer(content):
    # Handle either a string or Gemini's list of content blocks
    if isinstance(content, str):
        answer = content.strip()
    elif isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", "").strip())
            elif isinstance(item, str):
                parts.append(item)
        answer = "\n".join(part for part in parts if part)
    else:
        answer = str(content)

    print("\n\033[92m" + "─" * 50 + "\033[0m")
    print(" 💡 \033[1mAnswer\033[0m")
    print("\033[92m" + "─" * 50 + "\033[0m")
    type_text(answer, delay=0.005)
    print("\033[92m" + "─" * 50 + "\033[0m")

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL")

embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    embedding=embedding_model,
    collection_name="learning_rag"
)

llm = ChatGoogleGenerativeAI(
    model=model_name,
    google_api_key=api_key,
)

print_header()

user_query = input("🧑 Enter your question (or type 'exit' to quit): ").strip()

if user_query.lower() in ("exit", "quit"):
    print("\n👋 Goodbye! Thanks for using RAG Assistant.")
    sys.exit()

if not user_query:
    print("⚠️ Please enter a question.")
    sys.exit()

print("\n🔍 Searching your PDF for relevant information...")
search_results = vector_db.similarity_search(query=user_query)

context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])

SYSTEM_PROMPT = """You are a helpful AI assistant who a
nswers user's query based on available context retrieved 
from a PDF file along with page contents and page number. 
You should only answer the user based on the following context 
and navigate to user to open the right page to know more. 
return normal text dont return markdown files.
Context: {context}
"""

messages = [
    SystemMessage(content=SYSTEM_PROMPT.format(context=context)),
    HumanMessage(content=user_query)
]

response = llm.invoke(messages)

print("\n✨ Generating your answer...")
print_answer(response.content)

print("\n🎉 Thanks for using RAG Assistant!")