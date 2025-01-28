from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import re

from generator import GeneratorAgent
from retreive import Retriever

# ---------------------------------------------------------------------
# FastAPI Setup
# ---------------------------------------------------------------------
app = FastAPI(
    title="Scholarship Query API",
    description="API for querying DAAD scholarships and university programs."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with a specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------------
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class RetrievedChunk(BaseModel):
    score: float
    metadata: Dict[str, Any]

class QueryResponse(BaseModel):
    query: str
    response: str
    retrieved_chunks: List[RetrievedChunk]

# ---------------------------------------------------------------------
# Health Check Endpoint
# ---------------------------------------------------------------------
@app.get("/", summary="Health Check")
async def health_check():
    return {"message": "Scholarship Query API is running."}

# ---------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------
def fix_link_string(link_line: str) -> str:
    """
    Cleans up partial or spaced-out links, for example:
      'https: //example.com' -> 'https://example.com'
      '//example.com'        -> 'https://example.com'
    """
    link_line = link_line.strip()
    link_line = link_line.replace("https: //", "https://")
    link_line = link_line.replace("http: //", "http://")

    if link_line.startswith("//"):
        link_line = "https:" + link_line

    return link_line


def parse_chunk_data(data_str: Optional[str]) -> Dict[str, Any]:
    """
    Parses the chunk's data string line by line into a structured dictionary.

    Special Handling:
      1) If a line references "Submit Application", "the application form and further
         information can be found", or "we are looking forward to you application online",
         we treat the *next* line as a link (stored under "Submit Link").
      2) If a line references "For deadlines of the IMPACT Programme, please visit",
         we also treat the *next* line as a link (stored under "Submit Link").
      3) Otherwise, if a line is "Key: Value", we store {Key: Value}. BUT we also run 
         a regex on "Value" to see if there's one or more URLs in the text. If found:
           - We remove them from Value (or set it to "" if it was purely a link).
           - We store them under "Link" or "Links".
      4) If the entire line starts with http/https//, we store it as a single "Link" 
         (or a list if you prefer).
    """
    output: Dict[str, Any] = {}
    if not data_str:
        return output

    lines = data_str.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        lower_line = line.lower()

        # --- 1) SUBMIT APPLICATION / FURTHER INFO KEYWORDS ---
        if ("submit application" in lower_line
            or "the application form and further information can be found" in lower_line
            or "we are looking forward to you application online" in lower_line
            or "for deadlines of the impact programme, please visit" in lower_line):
            i += 1
            if i < len(lines):
                link_line = lines[i].strip()
                # If next line is a URL, store it under "Submit Link"
                if re.match(r'^(https?:|//)', link_line):
                    output["Submit Link"] = fix_link_string(link_line)
                else:
                    # Not a URL, store as raw text
                    output["Submit Link"] = link_line
            i += 1
            continue

        # --- 2) STANDALONE LINK (line starts with http, https, or //) ---
        if re.match(r'^(https?:|//)', line):
            # You could store multiple under a list, but let's do single "Link" for now
            output["Link"] = fix_link_string(line)
            i += 1
            continue

        # --- 3) KEY: VALUE ---
        parts = line.split(":", maxsplit=1)
        if len(parts) == 2:
            key = parts[0].strip()
            value = parts[1].strip()

            # a) Look for *any* links in the value using regex
            #    This finds all occurrences of "http://..." or "https://..."
            found_links = re.findall(r'(https?://\S+)', value)
            if found_links:
                # We'll remove the links from the text, 
                # and store them separately under a "Link" or "Links" key.
                cleaned_value = value
                for link in found_links:
                    cleaned_value = cleaned_value.replace(link, "").strip()

                # If there's exactly 1 link, store it under "Link"
                # If there's multiple, store them under "Links"
                if len(found_links) == 1:
                    # We'll store the single link under "Link"
                    # and also fix partial formatting
                    single_link = fix_link_string(found_links[0])
                    # Put into output
                    output.setdefault("Link", single_link)
                else:
                    # Multiple links
                    fixed_links = [fix_link_string(lk) for lk in found_links]
                    output.setdefault("Links", []).extend(fixed_links)

                # Now set the final cleaned text as the value
                # If the entire line was just the link(s), you might end up with ""
                value = cleaned_value

            # b) Store the key-value pair
            output[key] = value

        # If there's no colon, we skip or handle differently
        i += 1

    return output

# ---------------------------------------------------------------------
# Main Query Endpoint
# ---------------------------------------------------------------------
@app.post("/query", response_model=QueryResponse, summary="Query Scholarship Data")
async def query_scholarship_data(request: QueryRequest):
    """
    Query the scholarship dataset and retrieve the best matching chunks,
    then parse them for structured output.
    """
    try:
        # System prompt
        system_prompt = """<system_prompt>
        <description>
            You are a friendly and knowledgeable assistant specializing in DAAD scholarships and university programs.
            Your primary goal is to provide accurate and relevant answers to user queries based on the retrieved data chunks.
        </description>
        <rules>
            Always prioritize using the retrieved chunks to answer queries. Do not include any additional information 
            unless explicitly necessary.
            If the retrieved chunks lack sufficient information, answer using general knowledge only when it is 
            essential to address the user's query. Otherwise, inform the user that the information is not available.
            Maintain a conversational, friendly, and engaging tone in your responses while adhering to the facts.
            Return a well structured response
            Ensure that all outputs are returned in JSON format with the structure: {"answer": "String"}.
        </rules>
        </system_prompt>"""

        # 1) Retrieve top matching chunks
        retriever = Retriever(embedding_file="embeddings_metadata.json")
        retrieved_chunks = await retriever.retrieve_top_chunks(request.query, top_k=request.top_k)

        # 2) Generate the answer using the generator agent
        agent = GeneratorAgent()
        result = await agent.main_pipeline(request.query, retrieved_chunks, system_prompt)

        # 3) Parse each chunk's 'data' field
        parsed_chunks = []
        for chunk in result["retrieved_chunks"]:
            chunk_copy = chunk.copy()
            if "data" in chunk_copy["metadata"]:
                raw_data = chunk_copy["metadata"]["data"]
                chunk_copy["metadata"]["parsed_data"] = parse_chunk_data(raw_data)
            parsed_chunks.append(chunk_copy)

        # 4) Return the final response
        return {
            "query": request.query,
            "response": result["response"],
            "retrieved_chunks": parsed_chunks
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the query: {str(e)}"
        )
