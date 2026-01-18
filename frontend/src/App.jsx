import { useState } from 'react'
import './App.css'
import ChatInterface from './components/ChatInterface'

function App() {
  return (
    <div className="App">
      <header className="app-header">
        <h1>🤖 RAG Chatbot</h1>
        <p>Ask me anything based on your documents</p>
      </header>
      <ChatInterface />
    </div>
  )
}

export default App

