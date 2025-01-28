import openai
import pandas as pd
import json
import asyncio
from dotenv import load_dotenv
import os
load_dotenv()
openai_key = os.getenv("openAI_key")
openai.api_key = openai_key 

# qdrant_client = QdrantClient(
#     host="localhost",
#     port=6333,
#     check_version=False,
#     api_key="77cc0a53-1eda-4b61-af44-647ee8d42467"
# )


async def get_embedding(text, model="text-embedding-3-large"):
    response = openai.Embedding.create(input=text, model=model)
    return response['data'][0]['embedding']

def save_embeddings_and_metadata(embeddings, metadata, file_path="embeddings_metadata.json"):
    """
    Save embeddings and metadata to a JSON file.

    Parameters:
    - embeddings (list of lists): List of embedding vectors.
    - metadata (list of dict): List of metadata dictionaries.
    - file_path (str): File path to save the JSON file.
    """
    data_to_save = {"embeddings": embeddings, "metadata": metadata}
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data_to_save, file, ensure_ascii=False, indent=4)
    print(f"Embeddings and metadata saved to {file_path}")


def load_embeddings_and_metadata(file_path="embeddings_metadata.json"):
    """
    Load embeddings and metadata from a JSON file.

    Parameters:
    - file_path (str): File path of the JSON file to load.

    Returns:
    - tuple: A tuple containing a list of embeddings and a list of metadata.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data["embeddings"], data["metadata"]





def load_json_to_list(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                raise ValueError("JSON content is not a list.")
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return []

