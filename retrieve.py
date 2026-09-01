import chromadb
from embed import embed_chunks

def retrieve(question,n_results=3):
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection("rag-qa")

    question_embeding = embed_chunks([question]).tolist()

    result = collection.query(query_embeddings = question_embeding , n_results=n_results)
    return result["documents"][0] , result["distances"][0]

