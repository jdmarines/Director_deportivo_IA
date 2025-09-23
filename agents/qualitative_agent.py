import os
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain

# Asegúrate de que tu API Key de Gemini esté configurada en tus secretos/entorno
# from dotenv import load_dotenv
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY") -> Streamlit lo maneja automáticamente con st.secrets

class QualitativeAgent:
    """
    Agente experto en análisis cualitativo usando un sistema RAG.
    """
    def __init__(self, documents_path='data/articles'):
        print("Inicializando Agente Cualitativo...")
        
        # 1. Cargar los documentos desde la carpeta especificada
        loader = DirectoryLoader(documents_path, glob="**/*.txt", show_progress=True)
        self.documents = loader.load()
        print(f"Se cargaron {len(self.documents)} documentos.")
        
        # 2. Dividir los documentos en fragmentos (chunks) más pequeños
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        self.texts = text_splitter.split_documents(self.documents)
        print(f"Se dividieron los documentos en {len(self.texts)} fragmentos.")
        
        # 3. Crear los embeddings (vectores numéricos) para los fragmentos
        # Usamos un modelo popular y gratuito de Hugging Face
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
        print("Modelo de embeddings cargado.")
        
        # 4. Crear la base de datos vectorial (ChromaDB) con los fragmentos y sus embeddings
        # Esto crea la base de datos en memoria. No se guarda en disco para este MVP.
        self.vector_store = Chroma.from_documents(self.texts, self.embeddings)
        print("Base de datos vectorial creada en memoria.")
        
        # 5. Inicializar el LLM que generará las respuestas (Gemini)
        # Asegúrate de tener la API Key configurada en los secretos de Streamlit
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
        
        # 6. Crear la "cadena" de pregunta y respuesta
        self.chain = load_qa_chain(self.llm, chain_type="stuff")
        print("Agente Cualitativo listo. ✅")

    def answer_question(self, query: str) -> str:
        """
        Realiza una búsqueda de similitud y genera una respuesta basada en los documentos.
        """
        if not self.documents:
            return "No hay documentos cargados para realizar la búsqueda."
        
        print(f"Buscando documentos relevantes para la consulta: '{query}'")
        # a. Buscar en la base de datos vectorial los fragmentos más relevantes (Retrieval)
        relevant_docs = self.vector_store.similarity_search(query)
        
        print(f"Se encontraron {len(relevant_docs)} fragmentos relevantes.")
        
        # b. Ejecutar la cadena con la consulta y los documentos relevantes (Generation)
        response = self.chain.run(input_documents=relevant_docs, question=query)
        return response

# Ejemplo de uso (para probar el archivo directamente)
if __name__ == '__main__':
    # Esto asume que tienes la variable de entorno GOOGLE_API_KEY configurada
    # y una carpeta 'data/articles' con archivos .txt
    agent = QualitativeAgent()
    
    # Ejemplo de pregunta
    pregunta1 = "¿Hay algún reporte sobre la actitud profesional de Saka?"
    respuesta1 = agent.answer_question(pregunta1)
    print("\n--- Respuesta 1 ---")
    print(respuesta1)
    
    pregunta2 = "¿Qué dicen los informes sobre el rendimiento de Haaland?"
    respuesta2 = agent.answer_question(pregunta2)
    print("\n--- Respuesta 2 ---")
    print(respuesta2)
