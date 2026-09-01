import chromadb
from read_pdf import read_pdf
from chunk import split_text
from embed import embed_chunks

full_text = read_pdf("data/product_manual.pdf")
chunks = split_text(full_text)
embeddings = embed_chunks(chunks)

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("rag-qa")

ids = [str(i) for i in range(len(chunks))]


if collection.count() == 0:
    collection.add(
        documents = chunks,
        embeddings = embeddings.tolist(),
        ids = ids
    )

print(collection.count())