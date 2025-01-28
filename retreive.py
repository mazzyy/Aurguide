import openai
import numpy as np
import json
import asyncio
from dotenv import load_dotenv
import os
load_dotenv()
openai_key = os.getenv("openAI_key")
openai.api_key = openai_key 
# OpenAI API Key


class Retriever:
    def __init__(self, embedding_file="embeddings_metadata.json", model="text-embedding-ada-002"):
        self.embedding_file = embedding_file
        self.model = model
        self.embeddings = None
        self.metadata = None
        self.messages = [] 
        self._load_embeddings_and_metadata()

    def _load_embeddings_and_metadata(self):
        """
        Load embeddings and metadata from the specified file.
        """
        try:
            with open(self.embedding_file, "r", encoding="utf-8") as file:
                data = json.load(file)
            self.embeddings = np.array(data["embeddings"], dtype=np.float32)
            self.metadata = data["metadata"]
            print(f"Loaded {len(self.embeddings)} embeddings and metadata from {self.embedding_file}.")
        except FileNotFoundError:
            print(f"Error: The file '{self.embedding_file}' was not found.")
            self.embeddings = None
            self.metadata = None
        except json.JSONDecodeError:
            print(f"Error: Failed to parse JSON from the file '{self.embedding_file}'.")
            self.embeddings = None
            self.metadata = None
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.embeddings = None
            self.metadata = None

    async def _get_embedding(self, text):
        """
        Generate an embedding for the given text using OpenAI API.
        """
        try:
            response = await openai.Embedding.acreate(input=text, model=self.model)
            return response['data'][0]['embedding']
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None

    async def query(self, query_text, top_k=5):
        """
        Query the embeddings to find the most relevant chunks.
        """
        if self.embeddings is None or self.metadata is None:
            raise ValueError("Embeddings or metadata not loaded. Ensure the embedding file is correct.")

        query_embedding = await self._get_embedding(query_text)
        if query_embedding is None:
            raise RuntimeError("Failed to generate query embedding.")

        query_vector = np.array(query_embedding, dtype=np.float32)

        similarities = np.dot(self.embeddings, query_vector) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_vector)
        )

        # Filter results by score > 0.6 and sort by similarity
        filtered_results = [
            {"score": similarities[idx], "metadata": self.metadata[idx]}
            for idx in np.argsort(similarities)[::-1]
            if similarities[idx] > 0.75 
        ]

        return filtered_results[:top_k]

    async def retrieve_top_chunks(self, query_text, top_k=5):
        """
        Retrieve the top chunks for a given query.
        """
        try:
            return await self.query(query_text, top_k=top_k)
        except ValueError as ve:
            print(f"Error: {ve}")
            return []
        except RuntimeError as re:
            print(f"Error: {re}")
            return []
        except Exception as e:
            print(f"Unexpected error during retrieval: {e}")
            return []


# async def generate_response(query, retrieved_chunks, system_prompt, conversation_history):
#     """
#     Generate a response using GPT-4 based on the retrieved chunks, query, and conversation history.

#     Parameters:
#     - query (str): The user's query.
#     - retrieved_chunks (list): Top retrieved chunks with metadata.
#     - system_prompt (str): The system prompt for GPT-4.
#     - conversation_history (list): The conversation history to maintain continuity.

#     Returns:
#     - str: The generated response from the LLM.
#     """
#     # Prepare the retrieved context from chunks
#     context = "\n\n".join(
#         f"Chunk {idx + 1}:\n{chunk['metadata']['data']}" for idx, chunk in enumerate(retrieved_chunks)
#     )

#     # Add the user's query and retrieved context to conversation history
#     conversation_history.append({
#         "role": "user",
#         "content": f"<Query>{query}</Query>\n<Context>\n{context}</Context>"
#     })

#     # Include system prompt and conversation history in the request
#     messages = [{"role": "system", "content": system_prompt}] + conversation_history

#     try:
#         # Generate response using GPT-4
#         response = await openai.ChatCompletion.acreate(
#             model="gpt-4o-mini",
#             messages=messages
#         )

#         # Extract the LLM's response content
#         response_content = response['choices'][0]['message']['content']

#         # Add the assistant's response to conversation history
#         conversation_history.append({
#             "role": "assistant",
#             "content": response_content
#         })

#         return response_content

#     except Exception as e:
#         print(f"Error generating response: {e}")
#         return '{"answer": "An error occurred while generating the response."}'


# async def main_pipeline(query, embedding_file="embeddings_metadata.json", top_k=3):
#     """
#     Main pipeline to retrieve top chunks and generate a response.

#     Parameters:
#     - query (str): The user's query.
#     - embedding_file (str): Path to the embeddings file.
#     - top_k (int): Number of top chunks to retrieve.

#     Returns:
#     - dict: A dictionary containing the top chunks and the generated response.
#     """
#     system_prompt = """<system_prompt>
#     <description>
#         You are a friendly and knowledgeable assistant specializing in DAAD scholarships and university programs. 
#         Your primary goal is to provide accurate and relevant answers to user queries based on the retrieved data chunks.
#     </description>
#     <rules>
#         Always prioritize using the retrieved chunks to answer queries. Do not include any additional information 
#         unless explicitly necessary.
#         If the retrieved chunks lack sufficient information, answer using general knowledge only when it is 
#         essential to address the user's query. Otherwise, inform the user that the information is not available.
#         Maintain a conversational, friendly, and engaging tone in your responses while adhering to the facts.
#         Ensure that all outputs are returned in JSON format with the structure: {"answer": "..."}.
#     </rules>
# </system_prompt>"""

#     # Initialize retriever
#     retriever = Retriever(embedding_file=embedding_file)

#     # Retrieve top chunks
#     print(f"Retrieving top {top_k} chunks for the query: {query}")
#     retrieved_chunks = await retriever.retrieve_top_chunks(query, top_k=top_k)

#     # Generate response using GPT-4
#     print("Generating response using GPT-4...")
#     response = await generate_response(query, retrieved_chunks, system_prompt, retriever.messages)

#     return {
#         "query": query,
#         "retrieved_chunks": retrieved_chunks,
#         "response": response
#     }
