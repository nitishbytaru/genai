
from dotenv import load_dotenv
from mem0 import Memory
from google.genai.errors import ClientError
import os
import json
import time

# ----------------------------------------
# 1. LOAD ENVIRONMENT VARIABLES
# ----------------------------------------

print("\n========== MEM0 MEMORY AGENT ==========")

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

if not all([
    GEMINI_API_KEY,
    GEMINI_MODEL,
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_PASSWORD
]):
    raise ValueError("Missing environment variables!")

print("[SUCCESS] Environment variables loaded.")
print("[INFO] Gemini model:", GEMINI_MODEL)


# ----------------------------------------
# 2. MEM0 CONFIGURATION
# ----------------------------------------

config = {
    "version": "v1.1",

    "embedder": {
        "provider": "gemini",
        "config": {
            "api_key": GEMINI_API_KEY,
            "model": "models/gemini-embedding-001",
            "embedding_dims": 768
        }
    },

    "llm": {
        "provider": "gemini",
        "config": {
            "api_key": GEMINI_API_KEY,
            "model": GEMINI_MODEL
        }
    },

    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333,
            "collection_name": "memories_gemini_768",
            "embedding_model_dims": 768
        }
    },

    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": NEO4J_URI,
            "username": NEO4J_USERNAME,
            "password": NEO4J_PASSWORD
        }
    }
}


# ----------------------------------------
# 3. INITIALIZE MEM0
# ----------------------------------------

print("\n[INFO] Initializing Mem0...")

try:
    memory = Memory.from_config(config_dict=config)
    print("[SUCCESS] Mem0 initialized.")

except Exception as e:
    print("[ERROR] Initialization failed:", e)
    raise SystemExit(1)


# ----------------------------------------
# 4. MEMORY OPERATIONS
# ----------------------------------------

USER_ID = "nitish"

while True:

    print("\n========== MENU ==========")
    print("1. Add memory")
    print("2. Search memory")
    print("3. Exit")

    choice = input("\nChoose an option: ").strip()

    if choice == "3":
        print("[INFO] Application closed.")
        break

    try:

        # --------------------------------
        # ADD MEMORY
        # --------------------------------

        if choice == "1":

            user_message = input("\nEnter a fact to remember: ").strip()

            if not user_message:
                print("[WARNING] Empty message.")
                continue

            print("\n[INFO] Saving memory...")

            result = memory.add(
                messages=[
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                user_id=USER_ID
            )

            print("\n[SUCCESS] Memory saved.")

            print("\n========== MEM0 RESULT ==========")
            print(json.dumps(result, indent=2, default=str))

        # --------------------------------
        # SEARCH MEMORY
        # --------------------------------

        elif choice == "2":

            query = input("\nWhat do you want to remember? ").strip()

            if not query:
                print("[WARNING] Empty search query.")
                continue

            print("\n[INFO] Searching memories...")

            result = memory.search(
                query=query,
                user_id=USER_ID
            )

            print("\n========== SEARCH RESULTS ==========")

            results = result.get("results", [])

            if results:
                for item in results:
                    print("\nMemory:", item.get("memory"))
                    print("ID:", item.get("id"))
            else:
                print("[INFO] No matching memories found.")

        else:
            print("[WARNING] Invalid option.")
            continue

    except ClientError as e:
        print("\n[ERROR] Gemini API request failed.")
        print("[DETAILS]", e)
        print("[INFO] Check your Gemini quota and retry after the reset.")

    except Exception as e:
        print("\n[ERROR] Operation failed.")
        print("[DETAILS]", repr(e))

    # Avoid sending repeated requests too quickly.
    print("\n[INFO] Waiting 65 seconds before the next operation...")
    time.sleep(65)
