import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from django.conf import settings
from .sarvam import SarvamEmbeddings


def load_documents(data_path):
    """Load documents from the data directory."""
    documents = []
    
    # Load text files
    if os.path.exists(data_path):
        try:
            txt_loader = DirectoryLoader(
                data_path,
                glob="**/*.txt",
                loader_cls=TextLoader,
                show_progress=True
            )
            documents.extend(txt_loader.load())
        except Exception as e:
            print(f"Error loading text files: {e}")
        
        # Load PDF files
        try:
            pdf_loader = DirectoryLoader(
                data_path,
                glob="**/*.pdf",
                loader_cls=PyPDFLoader,
                show_progress=True
            )
            documents.extend(pdf_loader.load())
        except Exception as e:
            print(f"Error loading PDF files: {e}")
    
    return documents


def split_documents(documents):
    """Split documents into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    return chunks


def create_vectorstore(documents, persist_directory):
    """Create and persist a vector store from documents."""
    # Split documents into chunks
    chunks = split_documents(documents)
    
    if not chunks:
        print("No documents to process")
        return None
    
    # Create embeddings using Sarvam AI
    embeddings = SarvamEmbeddings(
        api_key=settings.SARVAM_API_KEY,
        model="sarvam-embed"  # Adjust model name as needed
    )
    
    # Create vector store
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    # Save vector store
    vectorstore.save_local(persist_directory)
    
    print(f"Created vector store with {len(chunks)} chunks")
    return vectorstore


def ingest_data(data_path=None):
    """Main function to ingest data and create vector store."""
    if data_path is None:
        data_path = os.path.join(settings.BASE_DIR, 'chatbot', 'data')
    
    persist_directory = settings.VECTORSTORE_PATH
    
    # Load documents
    print("Loading documents...")
    documents = load_documents(data_path)
    
    if not documents:
        print("No documents found. Please add documents to the data folder.")
        return None
    
    print(f"Loaded {len(documents)} documents")
    
    # Create vector store
    print("Creating vector store...")
    vectorstore = create_vectorstore(documents, persist_directory)
    
    return vectorstore


if __name__ == "__main__":
    ingest_data()
