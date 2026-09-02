# 智能文档问答系统（RAG）

个人主导实现的「读 PDF → 知识库检索 → 大模型回答」文档问答系统。核心是一条清晰可拆的 RAG 链路：用户上传 PDF 后，用自然语言提问，系统基于文档内容作答；检索不到相关内容时诚实回复「不知道」，绝不瞎编。

## 功能

- 📄 **PDF 解析**：上传 PDF，提取正文文本
- ✂️ **文本分块**：按块大小 + 重叠切分，保留上下文
- 🔍 **中文语义检索**：BGE 中文向量模型，解决英文模型对中文语义理解弱的问题
- 🧠 **大模型回答**：DeepSeek 基于检索到的文档块生成回答
- 🛡️ **安全护栏**：检索不到相关内容时诚实回复「不知道」（system prompt 软约束 + 相似度阈值硬约束，双保险）
- 🌐 **网页界面**：Streamlit 封装成交互式网页，方便演示验收

## 技术栈

| 技术 | 用途 |
|------|------|
| Python | 主语言 |
| PyMuPDF | 解析 PDF、提取文本 |
| sentence-transformers（BAAI/bge-small-zh-v1.5） | 中文语义向量化 |
| ChromaDB | 向量数据库，建索引 + 相似度检索 |
| DeepSeek | 大模型生成回答 |
| Streamlit | 网页界面 |

## 架构流程

```
上传 PDF
   ↓
提取文本（read_pdf）→ 分块（chunk）→ 向量化（embed）→ 建索引（store）
   ↓
用户提问
   ↓
相似度检索 top-k（retrieve）
   ↓
LLM 基于文档内容回答（answer）
   ↓
检索不到 → 诚实回复「不知道」（安全护栏）
```

## 项目结构

一条链路，一个文件干一件事：

```
rag-qa/
├── read_pdf.py     # 读 PDF 提取文本
├── chunk.py        # 文本分块（块大小 + 重叠）
├── embed.py        # 中文向量化（BGE）
├── store.py        # ChromaDB 建索引（持久化）
├── retrieve.py     # 相似度检索 top-k
├── answer.py       # LLM 回答 + 「不知道」阈值判断 + Prompt 约束
├── compare.py      # 中英文模型对比测试
├── app.py          # Streamlit 网页（全链路串联）
├── data/           # 待解析的 PDF 文档
├── chroma_db/      # 向量库持久化目录
└── requirements.txt
```

## 运行方法

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置 API key（在项目根目录新建 .env，写入你的 key）
echo "DEEPSEEK_API_KEY=你的密钥" > .env

# 3. 启动网页
streamlit run app.py
```

浏览器打开 http://localhost:8501 即可使用。

## 踩过的坑

- 英文向量模型（all-MiniLM-L6-v2）对中文语义检索不准：问「多少钱」会把含答案的块排到最后。换 BGE 中文模型（bge-small-zh-v1.5）后精准命中。
- 国内网络直连 HuggingFace 卡死：设置离线模式（HF_HUB_OFFLINE）让模型走本地缓存加载，避免一直「加载不出来」。
- ChromaDB 默认 embedding 从 AWS 下载模型超时：改为本地 SentenceTransformer 手动向量化后传入，绕过联网下载。
- top-k（n_results）调参：太小漏答案，太大引入无关块干扰，取 3 平衡。
- 相似度阈值判断：检索到的最相关块距离超过阈值时直接回复「不知道」，防止大模型瞎编。

## 关键词

RAG、向量检索、ChromaDB、Embedding、Prompt 调优

## 作者

hzy · 981233700@qq.com
