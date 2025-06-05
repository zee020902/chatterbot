import os
import sys
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PDFMinerLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 🔐 Load API key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# 🧠 LLM)
llm = ChatOpenAI(openai_api_key=openai_api_key, model_name="gpt-3.5-turbo",max_tokens=1000)

# 📁 Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(BASE_DIR, "my_doc.pdf")
vectorstore_path = os.path.join(BASE_DIR, "vectorstore")

# ✅ Make retrain_flag dynamic via CLI
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
        allow_dangerous_deserialization=True  # ✅ Add this line
    )


# 🔍 Create retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 💬 Main query function
def ask_query(query):
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    result = qa_chain({"query": query})

    if result["result"].lower().strip().startswith("i don't know") or not result["source_documents"]:
        return "This query is out of the scope of the documentation."
    return result["result"]
