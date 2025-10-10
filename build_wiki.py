"""
Build comprehensive wiki pages from cached documents
"""
from src.utils.database import DatabaseManager
from src.utils.embeddings import EmbeddingGenerator
from src.qa_system.rag_processor import RAGProcessor
from src.wiki.wiki_builder import WikiBuilder
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "src"))

# Initialize components
db_file = Path('data/user_data/medprep.db')
db_file.parent.mkdir(parents=True, exist_ok=True)

db = DatabaseManager(db_file)
emb_gen = EmbeddingGenerator()
rag = RAGProcessor(Path('data/cache'), emb_gen)

# Load the index first!
print('Loading RAG index...')
if not rag.load_index():
    print('❌ Failed to load RAG index. Run preprocess.py first.')
    exit(1)

print(f'✅ Loaded {len(rag.chunks)} chunks from index\n')

wiki = WikiBuilder(db, rag)

# Build wiki from documents
print('Building comprehensive wiki pages from cached documents...')
print('This will create detailed pages for all major USMLE topics...')
print()

wiki.build_wiki_from_documents([])

# Check results
pages = db.get_all_wiki_pages_by_system()
total = sum(len(p) for p in pages.values())

print(f'\n✅ Wiki build complete!')
print(f'Total pages created: {total}')
print('\nPages by system:')
for system, page_list in sorted(pages.items()):
    if page_list:
        print(f'  {system}: {len(page_list)} pages')
