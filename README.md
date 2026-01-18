# RAG Chatbot - Django + React + LangChain

A full-stack RAG (Retrieval-Augmented Generation) chatbot application built with Django backend, React frontend, and LangChain for LLM integration.

## Features

- 🤖 **RAG-based responses**: Uses document retrieval to provide accurate, context-aware answers
- 💬 **Conversational memory**: Maintains chat history for contextual conversations
- 📚 **Document ingestion**: Supports PDF and text files
- 🎨 **Modern UI**: Clean React interface with real-time chat
- 🔄 **CORS enabled**: Seamless frontend-backend communication

## Tech Stack

### Backend
- **Django 5.0**: Web framework
- **Django REST Framework**: API endpoints
- **LangChain**: LLM orchestration
- **OpenAI GPT-3.5**: Language model
- **FAISS**: Vector store for embeddings
- **python-dotenv**: Environment management

### Frontend
- **React 19**: UI framework
- **Vite**: Build tool
- **Axios**: HTTP client
- **CSS3**: Styling

## Project Structure

```
ChatBot/
├── backend/
│   ├── backend/          # Django project settings
│   ├── chatbot/          # Main Django app
│   │   ├── data/         # Documents for RAG (add your files here)
│   │   ├── rag/          # RAG implementation
│   │   │   ├── chain.py    # LangChain conversation chain
│   │   │   ├── ingest.py   # Document processing
│   │   │   └── prompts.py  # LLM prompts
│   │   ├── vectorstore/  # FAISS vector database (generated)
│   │   ├── views.py      # API endpoints
│   │   └── urls.py       # URL routing
│   ├── requirements.txt  # Python dependencies
│   └── .env             # Environment variables (create this)
└── frontend/
    ├── src/
    │   ├── components/
    │   │   └── ChatInterface.jsx
    │   ├── App.jsx
    │   └── App.css
    └── package.json
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API key

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On Mac/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file:**
   ```bash
   # Copy the example file
   copy .env.example .env  # On Windows
   # cp .env.example .env  # On Mac/Linux
   ```

5. **Add your OpenAI API key to .env:**
   ```
   OPENAI_API_KEY=your-actual-api-key-here
   ```

6. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

7. **Add your documents:**
   - Place PDF or TXT files in `chatbot/data/` folder
   - A sample document is already provided

8. **Ingest documents (create vector store):**
   ```bash
   python manage.py shell
   >>> from chatbot.rag.ingest import ingest_data
   >>> ingest_data()
   >>> exit()
   ```

9. **Start Django server:**
   ```bash
   python manage.py runserver
   ```
   Backend will run at `http://localhost:8000`

### Frontend Setup

1. **Open new terminal and navigate to frontend:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```
   Frontend will run at `http://localhost:5173`

## Usage

1. Open your browser and go to `http://localhost:5173`
2. Start chatting with the bot!
3. The bot will answer based on documents you added to the `data/` folder
4. Use the "Clear" button to reset conversation history

## API Endpoints

- `POST /api/chat/` - Send a message and get a response
- `POST /api/clear-history/` - Clear conversation history
- `POST /api/ingest/` - Re-ingest documents (use after adding new files)
- `GET /api/health/` - Health check

### Example API Request
```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"question": "What is RAG?"}'
```

## Adding New Documents

1. Add your PDF or TXT files to `backend/chatbot/data/`
2. Re-run the ingestion:
   ```bash
   python manage.py shell
   >>> from chatbot.rag.ingest import ingest_data
   >>> ingest_data()
   ```
   Or use the API endpoint:
   ```bash
   curl -X POST http://localhost:8000/api/ingest/
   ```

## Customization

### Change LLM Model
Edit `backend/chatbot/rag/chain.py`:
```python
self.llm = ChatOpenAI(
    model="gpt-4",  # Change to gpt-4 or other models
    temperature=0.7,
)
```

### Modify Prompts
Edit `backend/chatbot/rag/prompts.py` to customize how the bot responds.

### Adjust Chunk Size
Edit `backend/chatbot/rag/ingest.py`:
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Adjust chunk size
    chunk_overlap=200,
)
```

## Troubleshooting

**Issue**: "Vectorstore not found"
- **Solution**: Run the ingest script to create the vector store

**Issue**: "OpenAI API error"
- **Solution**: Check your API key in .env file and ensure you have credits

**Issue**: "CORS error"
- **Solution**: Ensure both frontend and backend are running and ports match the settings

**Issue**: "No documents found"
- **Solution**: Add documents to `backend/chatbot/data/` folder

## Environment Variables

Create a `.env` file in the `backend/` directory:
```
OPENAI_API_KEY=your-openai-api-key
```

## Production Deployment

1. Set `DEBUG=False` in settings.py
2. Update `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS`
3. Use production WSGI server (gunicorn)
4. Build React app: `npm run build`
5. Serve static files properly
6. Use environment variables for secrets

## License

This project is open source and available for educational purposes.

## Support

For issues and questions, please check:
- LangChain docs: https://python.langchain.com/
- Django docs: https://docs.djangoproject.com/
- React docs: https://react.dev/

## Next Steps

- Add user authentication
- Implement chat history persistence
- Add support for more document types
- Deploy to cloud platform
- Add streaming responses
- Implement chat sessions
