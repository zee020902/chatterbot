import os
import sys
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PDFMinerLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

# 🔐 Load API key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# 🧠 Initialize LLM
llm = ChatOpenAI(
    openai_api_key=openai_api_key,
    model_name="gpt-3.5-turbo",
    max_tokens=1000
)

# 📁 Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(BASE_DIR, "my_doc.pdf")
vectorstore_path = os.path.join(BASE_DIR, "vectorstore")

# ✅ Retrain flag
retrain_flag = "--retrain" in sys.argv

# 🔄 Load or create vectorstore
if retrain_flag or not os.path.exists(vectorstore_path):
    print("🔄 Processing and embedding PDF...")
    loader = PDFMinerLoader(pdf_path)
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = splitter.split_documents(pages)

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(vectorstore_path)
    print("✅ Embeddings stored!")
else:
    print("📦 Loading saved embeddings...")
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.load_local(
        vectorstore_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

# 🔍 Create retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# ✨ Strict prompt to ground in context
custom_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful assistant. Answer the following question **only using the provided context**.
If the answer is not contained in the context, say "I don't know" or "This query is out of the bounds of documentation."

Context:
{context}

Question:
{question}

Answer:
"""
)

# 💬 Main query function
def ask_query(query):
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": custom_prompt},
        return_source_documents=True
    )

    result = qa_chain({"query": query})
    answer = result["result"].strip().lower()

    if "i don't know" in answer or "out of the bounds" in answer or not result["source_documents"]:
        return "This query is out of the bounds of documentation."

    return result["result"]
