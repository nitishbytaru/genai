import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_qdrant import QdrantVectorStore
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    embedding=embedding_model,
    collection_name="learning_rag"
)

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL")

llm = ChatGoogleGenerativeAI(
    model=model_name,
    google_api_key=api_key,
)


def process_query(user_query: str):
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
    return response.content