"""
Embeddings utility for generating and managing document embeddings
"""
from sentence_transformers import SentenceTransformer
import torch

class EmbeddingGenerator:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        # Initialize device
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load model
        try:
            self.model = SentenceTransformer(model_name, device=self.device)
        except RuntimeError:
            # Fallback to CPU if GPU initialization fails
            self.device = "cpu"
            self.model = SentenceTransformer(model_name, device=self.device)
        
        self.embedding_size = 384  # Size for all-MiniLM-L6-v2
    
    def encode(self, texts, batch_size=32, show_progress=False):
        """Generate embeddings for a list of texts"""
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True
        )
        
        return embeddings
    
    def encode_single(self, text):
        """Generate embedding for a single text"""
        return self.encode([text])[0]
