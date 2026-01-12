import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import RetrievalQA

# 1. Load API Key
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    st.error("⚠️ .env file is missing or API KEY is not set!")
    st.stop()

# 2. UI Setup
st.set_page_config(page_title="Reliability RAG Agent", page_icon="🤖")
st.title("🤖 Self-Correcting RAG Agent")
st.markdown("""
### 🎯 Mission
This agent analyzes **technical documentation (PDF)** to provide accurate answers.
A built-in **'Critic Agent'** autonomously evaluates the reliability of the generated response.
""")

# 3. PDF File Upload
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    # Save uploaded file temporarily
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    with st.spinner("📄 Analyzing document..."):
        # Load PDF
        loader = PyPDFLoader("temp.pdf")
        pages = loader.load_and_split()
        # Chunking
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(pages)
        # Save to Vector DB (FAISS)
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(splits, embeddings)
        retriever = vectorstore.as_retriever()
        st.success(f"✅ Ingestion Complete! Processed ({len(splits)} chunks)")

    # 4. User Query Interface
    query = st.text_input("Enter your question:")
    
    if query:
        with st.spinner("🤔 Reasoning..."):
            llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
            
            # --- [Agent 1: Generator] Generate Answer ---
            qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)
            result = qa_chain.invoke({"query": query})
            answer = result['result']
            sources = result['source_documents']
            
            # --- [Agent 2: Critic] Evaluate Confidence ---
            critic_prompt = f"""
            You are a strict technical critic. Evaluate the answer based on the question.
            Question: {query}
            Answer: {answer}
            Rate confidence (1-10). If < 7, explain why.
            Format: [Confidence: X/10] Explanation
            """
            critic_response = llm.invoke(critic_prompt).content
            
        # 5. Display Results
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📝 Generator Answer")
            st.info(answer)
        with col2:
            st.subheader("🧐 Critic Evaluation")
            if "10/10" in critic_response or "9/10" in critic_response:
                st.success(critic_response)
            elif "8/10" in critic_response:
                st.info(critic_response)
            else:
                st.warning(critic_response)
        
        # Show Source Documents
        with st.expander("📚 View Source Evidence"):
            for doc in sources:
                st.write(f"- {doc.page_content[:300]}...")