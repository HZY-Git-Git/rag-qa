import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

import numpy as np
from sentence_transformers import SentenceTransformer
from read_pdf import read_pdf
from chunk import split_text

full_text = read_pdf("data/product_manual.pdf")
chunks = split_text(full_text)
query = "咖啡机多少钱"

def cosine(a,b):
    return np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))

for name in ["all-MiniLM-L6-v2","BAAI/bge-small-zh-v1.5"]:
    model = SentenceTransformer(name)
    qvec = model.encode(query)
    cvecs = model.encode(chunks)
    
    best_i = 0
    best_s = -1
    for i in range(len(chunks)):
        s = cosine(qvec, cvecs[i])
        if s > best_s:
            best_s = s
            best_i = i

    print(f"模型 {name}：最相似是第{best_i}块，相似度{best_s:.4f}")
    print(f"  内容：{chunks[best_i][:40]}")
        
         