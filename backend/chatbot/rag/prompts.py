from langchain_core.prompts import PromptTemplate

# System prompt for the RAG chatbot
SYSTEM_PROMPT = """You are a helpful AI assistant. Use the following context to answer the user's question.
If you cannot find the answer in the context, say so politely. Don't make up information.

Context: {context}

Question: {question}

Answer:"""

# Create the prompt template
QA_PROMPT = PromptTemplate(
    template=SYSTEM_PROMPT,
    input_variables=["context", "question"]
)

# Condensing question prompt for conversational retrieval
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(
    """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
)
