# --- INICIO DEL TRUCO PARA COMPATIBILIDAD CON SQLITE ---
# Este bloque es necesario para que chromadb funcione en Streamlit Cloud.
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# --- FIN DEL TRUCO ---

import os
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain

class QualitativeAgent:
    """
    Agente experto en análisis cualitativo usando un sistema RAG.
    """
    def __init__(self, documents_path='data/articles'):
        print("Inicializando Agente Cualitativo...")
        
        # El resto del código de la clase no cambia...
        loader = DirectoryLoader(documents_path, glob="**/*.txt", show_progress=True)
        self.documents = loader.load()
        print(f"Se cargaron {len(self.documents)} documentos.")
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        self.texts = text_splitter.split_documents(self.documents)
        print(f"Se dividieron los documentos en {len(self.texts)} fragmentos.")
        
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
        print("Modelo de embeddings cargado.")
        
        self.vector_store = Chroma.from_documents(self.texts, self.embeddings)
        print("Base de datos vectorial creada en memoria.")
        
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
        self.chain = load_qa_chain(self.llm, chain_type="stuff")
        print("Agente Cualitativo listo. ✅")

    def answer_question(self, query: str) -> str:
        if not self.documents:
            return "No hay documentos cargados para realizar la búsqueda."
        
        print(f"Buscando documentos relevantes para la consulta: '{query}'")
        relevant_docs = self.vector_store.similarity_search(query)
        print(f"Se encontraron {len(relevant_docs)} fragmentos relevantes.")
        
        response = self.chain.run(input_documents=relevant_docs, question=query)
        return response
