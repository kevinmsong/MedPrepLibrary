"""
RAG (Retrieval Augmented Generation) processor for context retrieval
"""
import json
import numpy as np
from pathlib import Path
import faiss
import nltk
from typing import List, Dict, Tuple

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

class RAGProcessor:
    def __init__(self, cache_dir, embedding_generator):
        self.cache_dir = Path(cache_dir)
        self.index_path = self.cache_dir / "faiss_index.idx"
        self.chunks_path = self.cache_dir / "text_chunks.json"
        self.embedding_generator = embedding_generator
        
        # Initialize FAISS index
        self.embedding_size = embedding_generator.embedding_size
        self.index = faiss.IndexFlatL2(self.embedding_size)
        self.chunks = []
    
    def chunk_text(self, text: str, chunk_size: int = 800, overlap: int = 100) -> List[str]:
        """Split text into overlapping chunks using NLTK's sentence tokenizer"""
        sentences = nltk.sent_tokenize(text)
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
            # If adding this sentence exceeds chunk_size, save current chunk
            if current_length + sentence_length > chunk_size and current_chunk:
                chunk_text = " ".join(current_chunk)
                chunks.append(chunk_text)
                
                # Create overlap by keeping last few sentences
                overlap_sentences = []
                overlap_length = 0
                for s in reversed(current_chunk):
                    if overlap_length + len(s) <= overlap:
                        overlap_sentences.insert(0, s)
                        overlap_length += len(s)
                    else:
                        break
                
                current_chunk = overlap_sentences
                current_length = overlap_length
            
            current_chunk.append(sentence)
            current_length += sentence_length
        
        # Add the last chunk
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
    
    def process_documents(self, documents: Dict[str, str]):
        """Process documents and create FAISS index"""
        try:
            print("Starting document processing...")
            all_chunks = []
            all_texts = []
            
            # Process each document
            total_chunks = 0
            for doc_name, content in documents.items():
                print(f"Processing {doc_name}...")
                chunks = self.chunk_text(content)
                total_chunks += len(chunks)
                print(f"Generated {len(chunks)} chunks from {doc_name}")
                
                # Store chunk metadata
                for chunk in chunks:
                    all_chunks.append({
                        "text": chunk,
                        "source": doc_name
                    })
                    all_texts.append(chunk)
            
            print(f"Total chunks processed: {total_chunks}")
            
            # Generate embeddings
            print("Generating embeddings...")
            embeddings = self.embedding_generator.encode(
                all_texts,
                batch_size=32,
                show_progress=True
            )
            
            # Convert to numpy array
            embeddings_array = np.array(embeddings).astype('float32')
            
            # Create FAISS index
            print("Creating FAISS index...")
            self.index = faiss.IndexFlatL2(self.embedding_size)
            self.index.add(embeddings_array)
            self.chunks = all_chunks
            
            # Save index and chunks
            print("Saving index and chunks...")
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            faiss.write_index(self.index, str(self.index_path))
            with open(self.chunks_path, 'w', encoding='utf-8') as f:
                json.dump(all_chunks, f, ensure_ascii=False, indent=2)
            
            print("Document processing complete!")
            return True
            
        except Exception as e:
            print(f"Error in process_documents: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def load_index(self) -> bool:
        """Load pre-built index and chunks"""
        try:
            if self.index_path.exists() and self.chunks_path.exists():
                print("Loading existing index...")
                self.index = faiss.read_index(str(self.index_path))
                with open(self.chunks_path, 'r', encoding='utf-8') as f:
                    self.chunks = json.load(f)
                print(f"Loaded {len(self.chunks)} chunks")
                return True
            return False
        except Exception as e:
            print(f"Error loading index: {str(e)}")
            return False
    
    def get_relevant_chunks(self, query: str, k: int = 5) -> List[Dict[str, str]]:
        """Retrieve k most relevant chunks for a query"""
        # Generate query embedding
        query_embedding = self.embedding_generator.encode_single(query)
        query_embedding = query_embedding.astype('float32').reshape(1, -1)
        
        # Search index
        distances, indices = self.index.search(query_embedding, k)
        
        # Get relevant chunks with metadata
        results = []
        for idx in indices[0]:
            if 0 <= idx < len(self.chunks):
                results.append(self.chunks[idx])
        
        return results
    
    def get_context_for_query(self, query: str, max_chunks: int = 5) -> Tuple[str, List[str]]:
        """Get relevant context and sources for a query"""
        chunks = self.get_relevant_chunks(query, k=max_chunks)
        context = "\n\n".join(chunk["text"] for chunk in chunks)
        sources = list(set(chunk["source"] for chunk in chunks))
        return context, sources
