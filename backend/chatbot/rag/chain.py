import os
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import HumanMessage, AIMessage
from django.conf import settings
from .prompts import QA_PROMPT, CONDENSE_QUESTION_PROMPT
from .sarvam import SarvamLLM, SarvamEmbeddings


class RAGChatbot:
    def __init__(self):
        self.llm = None
        self.vectorstore = None
        self.retriever = None
        self.chat_history = []
        self.initialize()
    
    def initialize(self):
        """Initialize the chatbot components."""
        # Initialize LLM with Sarvam AI
        self.llm = SarvamLLM(
            api_key=settings.SARVAM_API_KEY,
            model="sarvam-2b",  # Adjust model name as needed
            temperature=0.7,
            max_tokens=1024
        )
        
        # Load vector store
        try:
            embeddings = SarvamEmbeddings(
                api_key=settings.SARVAM_API_KEY,
                model="sarvam-embed"  # Adjust model name as needed
            )
            self.vectorstore = FAISS.load_local(
                settings.VECTORSTORE_PATH,
                embeddings,
                allow_dangerous_deserialization=True
            )
            
            # Create retriever
            self.retriever = self.vectorstore.as_retriever(
                search_kwargs={"k": 3}
            )
            
            print("RAG Chatbot initialized successfully")
        except Exception as e:
            print(f"Error initializing vectorstore: {e}")
            print("Please run ingest.py to create the vector store first")
    
    def get_response(self, question):
        """Get a response from the chatbot."""
        if not self.retriever:
            return {
                "answer": "Sorry, the chatbot is not initialized. Please ensure the vector store is created.",
                "source_documents": []
            }
        
        try:
            # Retrieve relevant documents
            docs = self.retriever.get_relevant_documents(question)
            
            # Format context from retrieved documents
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # Create prompt with context and question
            prompt_text = QA_PROMPT.format(context=context, question=question)
            
            # Get response from LLM
            answer = self.llm._call(prompt_text)
            
            # Add to chat history
            self.chat_history.append(HumanMessage(content=question))
            self.chat_history.append(AIMessage(content=answer))
            
            return {
                "answer": answer,
                "source_documents": [
                    {
                        "content": doc.page_content,
                        "metadata": doc.metadata
                    }
                    for doc in docs
                ]
            }
        except Exception as e:
            return {
                "answer": f"Error processing your question: {str(e)}",
                "source_documents": []
            }
    
    def clear_history(self):
        """Clear conversation history."""
        self.chat_history = []


# Global chatbot instance
_chatbot = None


def get_chatbot():
    """Get or create the global chatbot instance."""
    global _chatbot
    if _chatbot is None:
        _chatbot = RAGChatbot()
    return _chatbot
