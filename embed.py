import os
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

from read_pdf import read_pdf
from chunk import split_text
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-zh-v1.5")

def embed_chunks(chunks):
    embeddings = model.encode(chunks)
    return embeddings

if __name__ == "__main__":
    from read_pdf import read_pdf
    from chunk import split_text
    full_text = read_pdf("data/product_manual.pdf")
    chunks = split_text(full_text)
    embeddings = embed_chunks(chunks)
    print(len(embeddings))
    print(len(embeddings[0]))