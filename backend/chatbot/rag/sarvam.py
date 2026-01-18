import requests
import os
from typing import Any, List, Optional
from langchain_core.language_models.llms import LLM
from langchain_core.embeddings import Embeddings
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from django.conf import settings


class SarvamLLM(LLM):
    """Sarvam AI LLM wrapper for LangChain."""
    
    api_key: str
    model: str = "sarvam-2b"  # Default model
    temperature: float = 0.7
    max_tokens: int = 1024
    base_url: str = "https://api.sarvam.ai/v1"
    
    @property
    def _llm_type(self) -> str:
        return "sarvam"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Call Sarvam AI API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            # Extract response based on Sarvam AI's response format
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            elif "response" in result:
                return result["response"]
            else:
                return str(result)
                
        except requests.exceptions.RequestException as e:
            return f"Error calling Sarvam AI: {str(e)}"
    
    @property
    def _identifying_params(self) -> dict:
        """Get identifying parameters."""
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }


class SarvamEmbeddings(Embeddings):
    """Sarvam AI Embeddings wrapper for LangChain."""
    
    api_key: str
    model: str = "sarvam-embed"  # Default embedding model
    base_url: str = "https://api.sarvam.ai/v1"
    
    def __init__(self, api_key: str, model: str = "sarvam-embed"):
        self.api_key = api_key
        self.model = model
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents."""
        embeddings = []
        for text in texts:
            embedding = self._embed_single(text)
            embeddings.append(embedding)
        return embeddings
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query."""
        return self._embed_single(text)
    
    def _embed_single(self, text: str) -> List[float]:
        """Get embedding for a single text."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "input": text
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/embeddings",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            # Extract embedding based on Sarvam AI's response format
            if "data" in result and len(result["data"]) > 0:
                return result["data"][0]["embedding"]
            elif "embedding" in result:
                return result["embedding"]
            else:
                # Fallback: return a dummy embedding
                print(f"Warning: Unexpected response format from Sarvam AI: {result}")
                return [0.0] * 768  # Default embedding size
                
        except requests.exceptions.RequestException as e:
            print(f"Error getting embeddings from Sarvam AI: {str(e)}")
            return [0.0] * 768  # Return dummy embedding on error
