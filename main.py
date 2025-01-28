from retreive import main_pipeline



query_text = "What are the requirements for a civil engineering program in Germany?"

results = main_pipeline(query_text, embedding_file="embeddings_metadata.json", top_k=5)

# print("\n\n\nGenerated Response:")
# print(results["response"])


print("\n\nTop Retrieved Chunks:")
for idx, chunk in enumerate(results["retrieved_chunks"], start=1):
    
        # print(f"Chunk {idx}:")
        # print(f"Score: {chunk['score']:.4f}")
        # print(f"Data: {chunk['metadata']['data']}")
        print(f"Link: {chunk['metadata']['link']}")
        # print("-" * 50)
