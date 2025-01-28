import openai
import asyncio
import json
from dotenv import load_dotenv
import os
load_dotenv()
openai_key = os.getenv("openAI_key")
openai.api_key = openai_key 

class GeneratorAgent:
    def __init__(self, model="gpt-4o-mini"):
        """
        Initialize the generator agent with the specified OpenAI model.
        """
        self.model = model
        self.messages = []  # Conversation history

    async def generate_response(self, query, retrieved_chunks, system_prompt):
        """
        Generate a response using GPT-4 based on the retrieved chunks, query, and conversation history.

        Parameters:
        - query (str): The user's query.
        - retrieved_chunks (list): Top retrieved chunks with metadata.
        - system_prompt (str): The system prompt for GPT-4.

        Returns:
        - str: The generated response from the LLM.
        """
        # Prepare the retrieved context from chunks
        context = "\n\n".join(
            f"Chunk {idx + 1}:\n{chunk['metadata']['data']}" for idx, chunk in enumerate(retrieved_chunks)
        )

        # Add the user's query and retrieved context to conversation history
        self.messages.append({
            "role": "user",
            "content": f"<Query>{query}</Query>\n<Context>\n{context}</Context>"
        })

        # Include system prompt and conversation history in the request
        messages = [{"role": "system", "content": system_prompt}] + self.messages

        try:
            
            
            # Generate response using GPT-4
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
                response_format={ "type": "json_object" }
            )


            json_response_content = response['choices'][0]['message']['content']
            
            print(json_response_content)
            
            response_content = json_response_content
                       

         
            
            # response_content = response_content.get('answer')
        

            self.messages.append({
                "role": "assistant",
                "content": str(response_content)
            })

            print(f"length of messages: { len(self.messages) } " ) 

            return response_content

        except Exception as e:
            print(f"Error generating response: {e}")
            return '{"answer": "An error occurred while generating the response."}'


    async def main_pipeline(self, query, retrieved_chunks, system_prompt):
        """
        Main pipeline to generate a response based on the retrieved chunks and user query.

        Parameters:
        - query (str): The user's query.
        - retrieved_chunks (list): Retrieved chunks with metadata.
        - system_prompt (str): System prompt defining the agent's behavior.

        Returns:
        - dict: A dictionary containing the response and the conversation history.
        """
        try:
           
            # Generate response using GPT-4
            response = await self.generate_response(query, retrieved_chunks, system_prompt)

            return {
                "query": query,
                "response": response,
                "retrieved_chunks": retrieved_chunks
            }

        except Exception as e:
            print(f"Error in main_pipeline: {e}")
            # Return error response structure
            return {
                "query": query,
                "response": '{"answer": "An error occurred while processing your request."}',
                "retrieved_chunks": []
            }

