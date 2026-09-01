import streamlit as st
import chromadb
from read_pdf import read_pdf
from chunk import split_text
from embed import embed_chunks
from answer import answers

st.title("智能文档问答系统")

uploaded = st.file_uploader("上传PDF",type="pdf")

if uploaded is not None:
    path = "data/"+uploaded.name
    with open(path,"wb") as f:
        f.write(uploaded.getbuffer())

    full_text = read_pdf(path)
    chunks = split_text(full_text)
    embeddings = embed_chunks(chunks)

    client = chromadb.PersistentClient(path="./chroma_db")
    try:
        client.delete_collection("rag-qa")
    except Exception:
        pass
    collection = client.create_collection("rag-qa")

    ids = [str(i) for i in range(len(chunks))]

    collection.add(documents=chunks,embeddings=embeddings.tolist(),ids=ids)

    st.success(f"已建立索引，共{len(chunks)}块")

    question = st.text_input("请输入你的问题")
    if question :
        st.write(answers(question))