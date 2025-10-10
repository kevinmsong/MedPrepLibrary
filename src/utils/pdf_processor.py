"""
PDF processing utility for extracting text from medical textbooks
"""
import PyPDF2
from pathlib import Path
import json
import hashlib
import os
from tqdm import tqdm

class PDFProcessor:
    def __init__(self, pdf_dir, cache_dir):
        self.pdf_dir = Path(pdf_dir)
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def process_pdf(self, pdf_path):
        """Process a single PDF file and extract text"""
        pdf_path = Path(pdf_path)
        
        # Check cache first
        cache_key = self._get_cache_key(pdf_path)
        cache_path = self.cache_dir / f"{cache_key}.json"
        
        if cache_path.exists():
            print(f"Loading cached data for {pdf_path.name}")
            with open(cache_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        print(f"Processing {pdf_path.name}...")
        
        # Extract text from PDF
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            
            cache_data = {
                'filename': pdf_path.name,
                'num_pages': num_pages,
                'text': '',
                'pages': []
            }
            
            # Process pages with progress bar
            for i in tqdm(range(num_pages), desc=f"Processing {pdf_path.name}"):
                page = reader.pages[i]
                page_text = page.extract_text()
                
                cache_data['pages'].append({
                    'number': i + 1,
                    'text': page_text
                })
                cache_data['text'] += page_text + "\n"
            
            # Save to cache
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            print(f"Cached data for {pdf_path.name}")
            return cache_data
    
    def process_all_pdfs(self):
        """Process all PDFs in the directory"""
        pdf_files = list(self.pdf_dir.glob("*.pdf"))
        
        if not pdf_files:
            print("No PDF files found!")
            return {}
        
        all_documents = {}
        for pdf_file in pdf_files:
            data = self.process_pdf(pdf_file)
            all_documents[data['filename']] = data['text']
        
        return all_documents
    
    def _get_cache_key(self, pdf_path):
        """Generate a cache key based on filename and modification time"""
        mtime = os.path.getmtime(pdf_path)
        key_string = f"{pdf_path.name}_{mtime}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get_page_text(self, filename, page_number):
        """Get text from a specific page"""
        cache_files = list(self.cache_dir.glob("*.json"))
        
        for cache_file in cache_files:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data['filename'] == filename:
                    for page in data['pages']:
                        if page['number'] == page_number:
                            return page['text']
        
        return None
