import pathlib
import os
import streamlit as ui
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.chains import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter


# Configuration setup
load_dotenv()
google_api_key = os.environ.get("GOOGLE_API_KEY")

def initialize_app():
    ui.set_page_config(
        page_title="PDF Insight Assistant",
        page_icon="📄",
        layout="centered"
    )
    ui.sidebar.header("Document Management")
    ui.title("Interactive Document Analysis")
    ui.caption("Powered by Gemini AI")

def process_uploaded_files(uploaded_files):
    document_content = ""
    for file in uploaded_files:
        pdf_reader = PdfReader(file)
        for page in pdf_reader.pages:
            document_content += page.extract_text()
    return document_content

def chunk_content(full_text, chunk_size=8000, overlap=500):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap
    )
    return text_splitter.split_text(full_text)

def create_vector_index(text_segments):
    embedding_model = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001"
    )
    vector_db = FAISS.from_texts(text_segments, embedding_model)
    vector_db.save_local("vector_index")
    return vector_db

def create_conversation_chain():
    interaction_template = """Analyze the provided context thoroughly and answer the question comprehensively. 
    If the information isn't present in the context, explicitly state that the answer cannot be determined from the documents.
    
    Context: {context}
    Query: {question}
    
    Provide a detailed response:"""
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.2,
        client=genai
    )
    
    return load_qa_chain(
        llm=llm,
        chain_type="refine",
        prompt=PromptTemplate(
            template=interaction_template,
            input_variables=["context", "question"]
        )
    )

def handle_user_query(query):
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_db = FAISS.load_local("vector_index", embedding_model, allow_dangerous_deserialization=True)
    relevant_docs = vector_db.similarity_search(query)
    
    qa_chain = create_conversation_chain()
    response = qa_chain(
        {"input_documents": relevant_docs, "question": query},
        return_only_outputs=True
    )
    
    return response['output_text']

def reset_conversation():
    ui.session_state.messages = [
        {"role": "assistant", "content": "Upload documents to begin analysis"}
    ]

def main():
    initialize_app()
    
    with ui.sidebar:
        uploaded_docs = ui.file_uploader(
            "Select PDF documents",
            type="pdf",
            accept_multiple_files=True
        )
        
        if ui.button("Process Uploads", type="primary"):
            with ui.status("Analyzing documents..."):
                processed_text = process_uploaded_files(uploaded_docs)
                text_segments = chunk_content(processed_text)
                create_vector_index(text_segments)
                ui.success("Analysis complete")

    ui.sidebar.button("Clear History", on_click=reset_conversation)

    if "messages" not in ui.session_state:
        reset_conversation()

    for msg in ui.session_state.messages:
        with ui.chat_message(msg["role"]):
            ui.write(msg["content"])

    if user_input := ui.chat_input("Ask about your documents"):
        ui.session_state.messages.append({"role": "user", "content": user_input})
        
        with ui.chat_message("user"):
            ui.write(user_input)
        
        with ui.chat_message("assistant"):
            with ui.spinner("Generating response..."):
                ai_response = handle_user_query(user_input)
                ui.write(ai_response)
        
        ui.session_state.messages.append(
            {"role": "assistant", "content": ai_response}
        )

if __name__ == "__main__":
    main()