"""
MedPrepLibrary - Professional Medical Education Platform
AI-Powered USMLE Step 1 Preparation Tool with Gemini 2.5 Pro
"""
import streamlit as st
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.auth import check_authentication, show_login_page, logout
from src.utils.database import DatabaseManager
from src.utils.pdf_processor import PDFProcessor
from src.utils.embeddings import EmbeddingGenerator
from src.qa_system.rag_processor import RAGProcessor
from src.qa_system.gemini_qa import GeminiQA
from src.question_bank.question_manager import QuestionBankManager
from src.flashcards.flashcard_manager import FlashcardManager
from src.wiki.wiki_builder import WikiBuilder
from src.analytics.tracker import ProgressTracker

# Page configuration with zoom
st.set_page_config(
    page_title="MedPrepLibrary - USMLE Step 1 Prep",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS with enhanced readability
st.markdown("""
<style>
/* Import professional fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Sans+Pro:wght@400;600;700&display=swap');

/* Global font and spacing */
html, body, [class*="css"] {
    font-family: 'Inter', 'Source Sans Pro', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 16px;
    line-height: 1.6;
    color: #1a1a1a;
}

/* Main container */
.main .block-container {
    max-width: 1400px !important;
    padding: 2rem 3rem !important;
}

/* Hide sidebar */
[data-testid="stSidebar"], section[data-testid="stSidebar"] {
    display: none !important;
}

/* Professional color palette with better contrast */
:root {
    --primary-color: #1e3a5f;
    --primary-light: #2c5282;
    --secondary-color: #059669;
    --accent-color: #3b82f6;
    --background: #ffffff;
    --surface: #f8fafc;
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --border: #cbd5e1;
    --border-light: #e2e8f0;
}

/* Typography improvements */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.02em;
    margin-top: 1.5em;
    margin-bottom: 0.75em;
}

h1 { font-size: 2.25rem; line-height: 1.2; }
h2 { font-size: 1.875rem; line-height: 1.3; }
h3 { font-size: 1.5rem; line-height: 1.4; }

p, li, span {
    color: var(--text-secondary);
    line-height: 1.75;
    margin-bottom: 1em;
}

/* Header styling with better contrast */
.main-header {
    background: linear-gradient(135deg, #1e3a5f 0%, #2c5282 100%);
    color: white;
    padding: 2rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 2.5rem;
    box-shadow: 0 8px 24px rgba(30, 58, 95, 0.15);
}

.main-header h1 {
    margin: 0;
    font-size: 2.25rem;
    font-weight: 800;
    color: white;
    letter-spacing: -0.03em;
}

.main-header p {
    margin: 0.75rem 0 0 0;
    opacity: 0.95;
    font-size: 1.1rem;
    font-weight: 500;
}

/* Configuration panel - transparent */
.config-panel {
    background: transparent;
    border: none;
    padding: 0;
    margin-bottom: 2rem;

/* Enhanced button styling */
.stButton > button {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    border-radius: 10px;
    padding: 0.75rem 1.75rem;
    font-size: 1rem;
    border: 2px solid var(--primary-color);
    background-color: white;
    color: var(--primary-color);
    transition: all 0.2s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(30, 58, 95, 0.2);
    background-color: var(--primary-color);
    color: white;
}

.stButton > button[kind="primary"] {
    background-color: var(--primary-color);
    color: white;
    border: 2px solid var(--primary-color);
}

.stButton > button[kind="primary"]:hover {
    background-color: var(--primary-light);
    border-color: var(--primary-light);
    box-shadow: 0 8px 20px rgba(30, 58, 95, 0.25);
}

/* Wiki topic buttons - improved readability */
button[key^="wiki_topic_"] {
    padding: 0.65rem 1.25rem !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    text-align: left !important;
    border: 1.5px solid var(--border-light) !important;
    background-color: white !important;
    color: var(--text-primary) !important;
    line-height: 1.5 !important;
}

button[key^="wiki_topic_"]:hover {
    background-color: var(--surface) !important;
    border-color: var(--primary-color) !important;
    transform: translateX(6px) !important;
    box-shadow: 0 2px 8px rgba(30, 58, 95, 0.1) !important;
}

/* Input fields with better contrast */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    font-family: 'Inter', sans-serif;
    border-radius: 10px;
    border: 2px solid var(--border);
    padding: 0.875rem 1rem;
    font-size: 1rem;
    background-color: white;
    color: var(--text-primary);
    line-height: 1.6;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 4px rgba(30, 58, 95, 0.1);
    outline: none;
}

/* Select boxes */
.stSelectbox > div > div > div {
    font-family: 'Inter', sans-serif;
    border: 2px solid var(--border);
    border-radius: 10px;
    font-size: 1rem;
    background-color: white;
}

.stSelectbox > div > div > div:focus-within {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 4px rgba(30, 58, 95, 0.1);
}

/* Wiki content area - enhanced readability */
.wiki-content {
    background: white;
    padding: 2.5rem;
    border-radius: 12px;
    border: 2px solid var(--border-light);
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    line-height: 1.8;
    font-size: 1.05rem;
    color: var(--text-primary);
}

.wiki-content h1, .wiki-content h2, .wiki-content h3 {
    color: var(--text-primary);
    margin-top: 2rem;
    margin-bottom: 1rem;
    font-weight: 700;
}

.wiki-content p {
    margin-bottom: 1.25rem;
    line-height: 1.8;
}

.wiki-content ul, .wiki-content ol {
    margin-left: 1.5rem;
    margin-bottom: 1.25rem;
}

.wiki-content li {
    margin-bottom: 0.5rem;
    line-height: 1.75;
}

/* Expander styling */
.streamlit-expanderHeader {
    font-weight: 600;
    font-size: 1.05rem;
    color: var(--text-primary);
    background-color: var(--surface);
    border-radius: 10px;
    padding: 0.75rem 1rem;
}

/* Radio buttons */
.stRadio > div {
    gap: 0.75rem;
}

.stRadio > div > label {
    font-size: 1rem;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    border: 2px solid var(--border-light);
    background-color: white;
    transition: all 0.2s;
}

.stRadio > div > label:hover {
    border-color: var(--primary-color);
    background-color: var(--surface);
}

/* Alert messages with better contrast */
.stAlert {
    border-radius: 10px;
    border-width: 2px;
    font-weight: 500;
    padding: 1rem 1.25rem;
    font-size: 1rem;
}

.stSuccess {
    background-color: #d1fae5;
    border-color: #059669;
    color: #065f46;
}

.stInfo {
    background-color: #dbeafe;
    border-color: #3b82f6;
    color: #1e40af;
}

.stWarning {
    background-color: #fef3c7;
    border-color: #f59e0b;
    color: #92400e;
}

.stError {
    background-color: #fee2e2;
    border-color: #ef4444;
    color: #991b1b;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    # Authentication state - preserve across refreshes
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    
    # Other state variables
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "home"
    if 'gemini_api_key' not in st.session_state:
        st.session_state.gemini_api_key = None
    if 'qa_system' not in st.session_state:
        st.session_state.qa_system = None
    if 'question_bank_manager' not in st.session_state:
        st.session_state.question_bank_manager = None
    if 'flashcard_manager' not in st.session_state:
        st.session_state.flashcard_manager = None
    if 'wiki_builder' not in st.session_state:
        st.session_state.wiki_builder = None
    if 'progress_tracker' not in st.session_state:
        st.session_state.progress_tracker = None
    if 'db_manager' not in st.session_state:
        st.session_state.db_manager = None
    if 'rag_processor' not in st.session_state:
        st.session_state.rag_processor = None
    if 'embedding_generator' not in st.session_state:
        st.session_state.embedding_generator = None
    
    # Question bank state
    if 'current_question_set' not in st.session_state:
        st.session_state.current_question_set = []
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'question_responses' not in st.session_state:
        st.session_state.question_responses = {}
    if 'show_explanation' not in st.session_state:
        st.session_state.show_explanation = False
    
    # Flashcard state
    if 'current_flashcard_set' not in st.session_state:
        st.session_state.current_flashcard_set = []
    if 'current_flashcard_index' not in st.session_state:
        st.session_state.current_flashcard_index = 0
    if 'show_flashcard_back' not in st.session_state:
        st.session_state.show_flashcard_back = False

def initialize_system():
    """Initialize all system components"""
    if st.session_state.initialized:
        return True
    
    try:
        # Get paths
        base_dir = Path(__file__).parent
        data_dir = base_dir / "data"
        cache_dir = data_dir / "cache"
        user_data_dir = data_dir / "user_data"
        
        # Create directories
        for directory in [cache_dir, user_data_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        db_path = user_data_dir / "medprep.db"
        st.session_state.db_manager = DatabaseManager(str(db_path))
        
        # Initialize embedding generator
        st.session_state.embedding_generator = EmbeddingGenerator()
        
        # Initialize RAG processor
        st.session_state.rag_processor = RAGProcessor(
            cache_dir=str(cache_dir),
            embedding_generator=st.session_state.embedding_generator
        )
        
        # Load existing index
        st.session_state.rag_processor.load_index()
        
        # Initialize managers
        st.session_state.question_bank_manager = QuestionBankManager(
            st.session_state.db_manager,
            st.session_state.rag_processor,
            None  # gemini_qa will be set when API key is provided
        )
        
        st.session_state.flashcard_manager = FlashcardManager(
            st.session_state.db_manager,
            st.session_state.rag_processor,
            None  # gemini_qa will be set when API key is provided
        )
        
        st.session_state.wiki_builder = WikiBuilder(
            st.session_state.db_manager,
            st.session_state.rag_processor
        )
        
        st.session_state.progress_tracker = ProgressTracker(st.session_state.db_manager)
        
        st.session_state.initialized = True
        return True
        
    except Exception as e:
        st.error(f"❌ System initialization error: {str(e)}")
        return False

def initialize_gemini():
    """Initialize Gemini QA system with API key"""
    if not st.session_state.gemini_api_key:
        return False
    
    try:
        st.session_state.qa_system = GeminiQA(st.session_state.gemini_api_key)
        # Update managers with gemini instance
        if st.session_state.question_bank_manager:
            st.session_state.question_bank_manager.gemini = st.session_state.qa_system
        if st.session_state.flashcard_manager:
            st.session_state.flashcard_manager.gemini = st.session_state.qa_system
        return True
    except Exception as e:
        st.error(f"❌ Gemini initialization error: {str(e)}")
        return False

def show_header():
    """Show main header with navigation"""
    st.markdown("""
    <div class="main-header">
        <h1>🏥 MedPrepLibrary</h1>
        <p>Your AI-Powered USMLE Step 1 Companion | Powered by Gemini 2.5 Pro</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation buttons in header
    st.markdown("---")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("🏠 Home", key="nav_home_header", width="stretch"):
            st.session_state.current_page = "home"
            st.rerun()
    
    with col2:
        if st.button("❓ Ask", key="nav_qa_header", width="stretch"):
            st.session_state.current_page = "qa"
            st.rerun()
    
    with col3:
        if st.button("📖 Wiki", key="nav_wiki_header", width="stretch"):
            st.session_state.current_page = "wiki"
            st.rerun()
    
    with col4:
        if st.button("📝 Questions", key="nav_qbank_header", width="stretch"):
            st.session_state.current_page = "question_bank"
            st.rerun()
    
    with col5:
        if st.button("🎴 Flashcards", key="nav_flashcards_header", width="stretch"):
            st.session_state.current_page = "flashcards"
            st.rerun()
    
    with col6:
        if st.button("📊 Analytics", key="nav_analytics_header", width="stretch"):
            st.session_state.current_page = "analytics"
            st.rerun()
    
    st.markdown("---")

def show_config_panel():
    """Show configuration panel with API key and user info"""
    # Compact config bar
    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
    
    with col1:
        # API Key input
        api_key_input = st.text_input(
            "⚙️ Gemini API Key",
            type="password",
            value=st.session_state.gemini_api_key or "",
            help="Get your free API key from https://aistudio.google.com/app/apikey",
            key="api_key_input",
            label_visibility="collapsed",
            placeholder="Enter Gemini API Key (starts with AIza...)"
        )
    
    with col2:
        if st.button("💾 Save API Key", key="save_api_key", width="stretch"):
            if api_key_input and api_key_input.strip():
                api_key_input = api_key_input.strip()
                if not api_key_input.startswith("AIza"):
                    st.error("❌ Invalid API key format. Gemini API keys start with 'AIza'")
                else:
                    st.session_state.gemini_api_key = api_key_input
                    st.session_state.qa_system = None  # Force reinitialization
                    if initialize_gemini():
                        st.success("✅ API key saved and validated!")
                        st.rerun()
                    else:
                        st.session_state.gemini_api_key = ""
                        st.error("❌ API key validation failed. Please check your key and try again.")
            else:
                st.warning("⚠️ Please enter an API key")
    
    with col3:
        # Status indicator
        if st.session_state.gemini_api_key and st.session_state.qa_system:
            st.markdown('<div style="padding: 0.5rem; text-align: center;"><span class="status-badge status-success">✅ AI Active</span></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="padding: 0.5rem; text-align: center;"><span class="status-badge status-warning">⚠️ AI Inactive</span></div>', unsafe_allow_html=True)
    
    with col4:
        if st.button("🚪 Logout", key="logout_button", width="stretch"):
            logout()
            st.rerun()

def show_home_page():
    """Show home page with navigation"""
    show_header()
    show_config_panel()
    
    # Welcome message
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0;">
        <h2>Welcome back, {st.session_state.username}! 👋</h2>
        <p style="font-size: 1.1rem; color: #6C757D;">Choose a feature below to continue your USMLE preparation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature overview
    st.markdown("---")
    st.markdown("""
    ### 🎯 Available Features
    
    Use the navigation buttons at the top to access:
    
    **❓ Ask Question**: Get AI-powered answers to any medical question using RAG (Retrieval Augmented Generation) 
    with Gemini 2.5 Pro. All answers are grounded in authoritative medical sources from First Aid.
    
    **📖 Medical Wiki**: Browse our comprehensive knowledge base of 370 medical topics organized across 15 systems. 
    All content is extracted from First Aid for the USMLE Step 1 with an intuitive clickable ontology.
    
    **📝 Question Bank**: Generate and practice USMLE-style questions *(Coming Soon)*
    
    **🎴 Flashcards**: Study with spaced repetition learning *(Coming Soon)*
    
    **📊 Analytics**: Track your progress and performance *(Coming Soon)*
    
    ---
    
    ### 🚀 Getting Started
    
    1. **Enter your Gemini API key** in the configuration panel above (get one free at [Google AI Studio](https://aistudio.google.com/app/apikey))
    2. **Click any navigation button** at the top to start using the platform
    3. **Ask questions** or **browse the wiki** to begin your USMLE preparation
    
    💡 **Tip**: Your session is saved - you can navigate freely without logging out!
    """)

# Import page functions from original app
# (We'll keep the existing page implementations)


def show_qa_page():
    """Show Question Answering page"""
    st.markdown("## ❓ Ask a Question")
    
    if not st.session_state.qa_system:
        st.warning("⚠️ Please enter your Gemini API key in the Configuration panel above to use this feature.")
        return
    
    question = st.text_area("Enter your medical question:", height=100, placeholder="e.g., What are the stages of hypertension?")
    
    if st.button("🔍 Get Answer", type="primary"):
        if question:
            with st.spinner("Searching knowledge base and generating answer..."):
                try:
                    # Get relevant context from RAG
                    context_chunks = st.session_state.rag_processor.get_relevant_chunks(question, k=5)
                    context = "\n\n".join([chunk['text'] for chunk in context_chunks])
                    
                    # Get answer from Gemini
                    answer = st.session_state.qa_system.get_answer(question, context)
                    st.markdown("### 💡 Answer")
                    st.markdown(answer)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a question.")

def show_wiki_page():
    """Show Medical Wiki browser with expanded ontology"""
    st.markdown("## 📖 Medical Wiki")
    st.markdown("Browse 370 comprehensive medical topics organized by system")
    
    # Ensure database is initialized
    if not st.session_state.db_manager:
        st.error("Database not initialized. Please contact support.")
        return
    
    try:
        # Get pages organized by system
        systems = st.session_state.db_manager.get_all_wiki_pages_by_system()
        
        if not systems or len(systems) == 0:
            st.warning("⚠️ Wiki database is empty or not loaded properly.")
            st.info("The wiki contains 370 medical topics. If you're seeing this message, there may be a database issue.")
            return
        
        # Initialize selected topic in session state
        if 'selected_wiki_topic' not in st.session_state:
            st.session_state.selected_wiki_topic = None
        
        # Create two columns: ontology on left, content on right
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### 📑 Medical Systems")
            st.markdown("---")
            
            # Display expanded ontology
            for system in sorted(systems.keys()):
                # System header with expander
                with st.expander(f"**{system}** ({len(systems[system])} topics)", expanded=True):
                    # Display all topics as clickable buttons
                    for page in sorted(systems[system], key=lambda x: x['title']):
                        topic_title = page['title']
                        # Create a unique button for each topic
                        if st.button(
                            f"📄 {topic_title}", 
                            key=f"wiki_topic_{topic_title}",
                            width="stretch"
                        ):
                            st.session_state.selected_wiki_topic = topic_title
                            st.rerun()
        
        with col2:
            if st.session_state.selected_wiki_topic:
                # Get the full page content
                page_data = st.session_state.db_manager.get_wiki_page(st.session_state.selected_wiki_topic)
                if page_data:
                    st.markdown(f"""
                    <div class="wiki-content">
                        <h1>{page_data['title']}</h1>
                        <p style="color: #64748b; font-style: italic; margin-bottom: 2rem;">System: {page_data['system']}</p>
                        <hr style="border: none; border-top: 2px solid #e2e8f0; margin: 2rem 0;">
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Content with enhanced readability
                    st.markdown(f'<div class="wiki-content">{page_data["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.error("Could not load page content.")
            else:
                # Show welcome message
                st.markdown("""
                ### Welcome to the Medical Wiki! 👋
                
                This comprehensive medical knowledge base contains **370 topics** across **15 medical systems**, 
                extracted from First Aid for the USMLE Step 1.
                
                **How to use:**
                1. Browse the medical systems in the left panel
                2. Click on any topic to view its detailed content
                3. All content is document-faithful and sourced from authoritative medical texts
                
                **Available Systems:**
                """)
                
                # Show system summary
                for system in sorted(systems.keys()):
                    st.markdown(f"- **{system}**: {len(systems[system])} topics")
                
                st.markdown("---")
                st.info("💡 **Tip:** Click on any topic in the left panel to get started!")
                
    except Exception as e:
        st.error(f"Error loading wiki: {str(e)}")

def show_question_bank_page():
    """Show Question Bank page"""
    st.markdown("## 📝 Question Bank")
    st.markdown("Generate USMLE-style practice questions from the knowledge base")
    
    if not st.session_state.qa_system:
        st.warning("⚠️ Please enter your Gemini API key in the Configuration panel to generate questions.")
        return
    
    # Initialize question set in session state
    if 'generated_questions' not in st.session_state:
        st.session_state.generated_questions = []
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False
    
    # Question generation interface
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Get all systems for dropdown
        try:
            systems = st.session_state.db_manager.get_all_wiki_pages_by_system()
            if systems and len(systems) > 0:
                system_list = ["Any System"] + sorted(systems.keys())
            else:
                system_list = ["Any System", "Cardiovascular", "Respiratory", "Gastrointestinal", 
                              "Renal", "Endocrine", "Hematology", "Immunology", "Neurology",
                              "Psychiatry", "Musculoskeletal", "Dermatology", "Reproductive",
                              "Biochemistry", "Microbiology", "Pharmacology"]
        except:
            system_list = ["Any System", "Cardiovascular", "Respiratory", "Gastrointestinal", 
                          "Renal", "Endocrine", "Hematology", "Immunology", "Neurology",
                          "Psychiatry", "Musculoskeletal", "Dermatology", "Reproductive",
                          "Biochemistry", "Microbiology", "Pharmacology"]
        
        selected_system = st.selectbox("Medical System:", system_list)
    
    with col2:
        topic = st.text_input("Specific Topic (optional):", placeholder="e.g., Hypertension")
    
    with col3:
        difficulty = st.selectbox("Difficulty:", ["Easy", "Medium", "Hard"])
    
    if st.button("🎲 Generate 10 Questions", type="primary", width="stretch"):
        st.session_state.generated_questions = []
        st.session_state.user_answers = {}
        st.session_state.show_results = False
        
        with st.spinner("Generating 10 USMLE-style questions... This may take a minute."):
            try:
                # Get relevant context
                if topic:
                    query = topic
                elif selected_system != "Any System":
                    query = selected_system
                else:
                    query = "medical knowledge"
                
                context_chunks = st.session_state.rag_processor.get_relevant_chunks(query, k=10)
                context = "\n\n".join([chunk['text'] for chunk in context_chunks])
                
                # Generate 10 questions
                for i in range(10):
                    question_data = st.session_state.qa_system.generate_question(
                        context=context,
                        topic=topic if topic else selected_system,
                        system=selected_system if selected_system != "Any System" else "General",
                        difficulty=difficulty.lower()
                    )
                    
                    if question_data:
                        st.session_state.generated_questions.append(question_data)
                
                if st.session_state.generated_questions:
                    st.success(f"✅ Generated {len(st.session_state.generated_questions)} questions!")
                    st.rerun()
                else:
                    st.error("Failed to generate questions. Please try again.")
                    
            except Exception as e:
                st.error(f"Error generating questions: {str(e)}")
    
    # Display generated questions
    if st.session_state.generated_questions:
        st.markdown("---")
        st.markdown(f"### 📋 Question Set ({len(st.session_state.generated_questions)} Questions)")
        
        for idx, question_data in enumerate(st.session_state.generated_questions, 1):
            with st.expander(f"**Question {idx}**", expanded=(idx == 1)):
                st.markdown(f"**{question_data.get('question_text', '')}**")
                st.markdown("")
                
                options = question_data.get('options', {})
                
                # Create radio buttons for answer selection
                answer_key = f"q_{idx}_answer"
                user_answer = st.radio(
                    "Select your answer:",
                    options=list(options.keys()),
                    format_func=lambda x: f"{x}. {options[x]}",
                    key=answer_key
                )
                
                st.session_state.user_answers[idx] = user_answer
                
                if st.button(f"✅ Check Answer", key=f"check_{idx}"):
                    correct_answer = question_data.get('correct_answer', '')
                    
                    if user_answer == correct_answer:
                        st.success(f"🎉 Correct! The answer is **{correct_answer}**.")
                    else:
                        st.error(f"❌ Incorrect. The correct answer is **{correct_answer}**.")
                    
                    st.markdown("**💡 Explanation:**")
                    st.info(question_data.get('explanation', ''))
        
        # Show overall results button
        if st.button("📊 Show Overall Results", type="primary", width="stretch"):
            st.session_state.show_results = True
            st.rerun()
        
        if st.session_state.show_results:
            correct_count = 0
            for idx, question_data in enumerate(st.session_state.generated_questions, 1):
                if st.session_state.user_answers.get(idx) == question_data.get('correct_answer'):
                    correct_count += 1
            
            score_pct = (correct_count / len(st.session_state.generated_questions)) * 100
            st.markdown("---")
            st.markdown("### 🎯 Your Results")
            st.metric("Score", f"{correct_count}/{len(st.session_state.generated_questions)} ({score_pct:.1f}%)")
    
    # Show some stats
    st.markdown("---")
    st.markdown("### 📊 Your Question Bank Stats")
    try:
        stats = st.session_state.db_manager.get_user_statistics(st.session_state.user_id)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Questions Answered", stats.get('total_questions', 0))
        with col2:
            st.metric("Correct Answers", stats.get('correct_answers', 0))
        with col3:
            accuracy = stats.get('accuracy', 0)
            st.metric("Accuracy", f"{accuracy:.1f}%")
    except:
        st.info("Start answering questions to see your statistics!")

def show_flashcards_page():
    """Show Flashcards page"""
    st.markdown("## 🎴 Flashcards")
    st.markdown("Study medical concepts with interactive flashcards")
    
    if not st.session_state.qa_system:
        st.warning("⚠️ Please enter your Gemini API key in the Configuration panel to generate flashcards.")
        return
    
    # Initialize flashcard state
    if 'current_flashcard' not in st.session_state:
        st.session_state.current_flashcard = None
    if 'show_answer' not in st.session_state:
        st.session_state.show_answer = False
    
    # Flashcard generation interface
    st.markdown("### 📚 Generate New Flashcard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Get all systems for dropdown
        try:
            systems = st.session_state.db_manager.get_all_wiki_pages_by_system()
            if systems and len(systems) > 0:
                system_list = ["Any System"] + sorted(systems.keys())
            else:
                system_list = ["Any System", "Cardiovascular", "Respiratory", "Gastrointestinal", 
                              "Renal", "Endocrine", "Hematology", "Immunology", "Neurology",
                              "Psychiatry", "Musculoskeletal", "Dermatology", "Reproductive",
                              "Biochemistry", "Microbiology", "Pharmacology"]
        except:
            system_list = ["Any System", "Cardiovascular", "Respiratory", "Gastrointestinal", 
                          "Renal", "Endocrine", "Hematology", "Immunology", "Neurology",
                          "Psychiatry", "Musculoskeletal", "Dermatology", "Reproductive",
                          "Biochemistry", "Microbiology", "Pharmacology"]
        
        selected_system = st.selectbox("Medical System:", system_list, key="flashcard_system")
    
    with col2:
        topic = st.text_input("Specific Topic (optional):", placeholder="e.g., Pharmacology", key="flashcard_topic")
    
    if st.button("✨ Generate Flashcard", type="primary", width="stretch"):
        with st.spinner("Creating flashcard..."):
            try:
                # Get relevant context
                if topic:
                    query = topic
                elif selected_system != "Any System":
                    query = selected_system
                else:
                    query = "medical knowledge"
                
                context_chunks = st.session_state.rag_processor.get_relevant_chunks(query, k=2)
                context = "\n\n".join([chunk['text'] for chunk in context_chunks])
                
                # Generate flashcard using GeminiQA
                flashcard_data = st.session_state.qa_system.generate_flashcard(
                    context=context,
                    topic=topic if topic else selected_system
                )
                
                if flashcard_data:
                    st.session_state.current_flashcard = flashcard_data
                    st.session_state.show_answer = False
                    st.rerun()
                else:
                    st.error("Failed to generate flashcard. Please try again.")
                    
            except Exception as e:
                st.error(f"Error generating flashcard: {str(e)}")
    
    # Display current flashcard
    if st.session_state.current_flashcard:
        st.markdown("---")
        st.markdown("### 🎯 Current Flashcard")
        
        # Flashcard container
        flashcard = st.session_state.current_flashcard
        
        # Front of card (question/term)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 3rem; 
                    border-radius: 15px; 
                    text-align: center; 
                    color: white; 
                    font-size: 1.5rem; 
                    font-weight: bold;
                    min-height: 200px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
            {flashcard.get('front', 'No question available')}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Show/Hide answer button
        if not st.session_state.show_answer:
            if st.button("👁️ Show Answer", width="stretch", type="primary"):
                st.session_state.show_answer = True
                st.rerun()
        else:
            # Back of card (answer)
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 2rem; 
                        border-radius: 15px; 
                        color: white; 
                        font-size: 1.1rem;
                        min-height: 150px;
                        box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
                <strong>Answer:</strong><br><br>
                {flashcard.get('back', 'No answer available')}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Rating buttons
            st.markdown("### 📊 How well did you know this?")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("😕 Hard", width="stretch"):
                    st.session_state.show_answer = False
                    st.success("Marked as Hard - Review again soon!")
            
            with col2:
                if st.button("🙂 Good", width="stretch"):
                    st.session_state.show_answer = False
                    st.success("Marked as Good!")
            
            with col3:
                if st.button("😄 Easy", width="stretch"):
                    st.session_state.show_answer = False
                    st.success("Marked as Easy!")
    else:
        st.info("👆 Generate a flashcard to start studying!")

def show_analytics_page():
    """Show Analytics/Progress page"""
    st.markdown("## 📊 Progress Analytics")
    st.markdown(f"Track your learning progress, {st.session_state.username}!")
    
    # Overall statistics
    st.markdown("### 📈 Overall Statistics")
    
    try:
        # Get wiki pages count
        systems = st.session_state.db_manager.get_all_wiki_pages_by_system()
        total_topics = sum(len(topics) for topics in systems.values())
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1.5rem; 
                        border-radius: 10px; 
                        text-align: center; 
                        color: white;">
                <h2 style="margin: 0; font-size: 2.5rem;">370</h2>
                <p style="margin: 0.5rem 0 0 0;">Wiki Topics</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 1.5rem; 
                        border-radius: 10px; 
                        text-align: center; 
                        color: white;">
                <h2 style="margin: 0; font-size: 2.5rem;">15</h2>
                <p style="margin: 0.5rem 0 0 0;">Medical Systems</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                        padding: 1.5rem; 
                        border-radius: 10px; 
                        text-align: center; 
                        color: white;">
                <h2 style="margin: 0; font-size: 2.5rem;">∞</h2>
                <p style="margin: 0.5rem 0 0 0;">Questions Available</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
                        padding: 1.5rem; 
                        border-radius: 10px; 
                        text-align: center; 
                        color: white;">
                <h2 style="margin: 0; font-size: 2.5rem;">∞</h2>
                <p style="margin: 0.5rem 0 0 0;">Flashcards Available</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # System breakdown
        st.markdown("### 🏥 Medical Systems Coverage")
        
        system_data = []
        for system, topics in sorted(systems.items()):
            system_data.append({
                "System": system,
                "Topics": len(topics),
                "Coverage": "✅ Complete"
            })
        
        import pandas as pd
        df = pd.DataFrame(system_data)
        st.dataframe(df, width="stretch", hide_index=True)
        
        st.markdown("---")
        
        # Study recommendations
        st.markdown("### 💡 Study Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 🎯 Recommended Study Plan
            
            1. **Browse the Wiki** - Start with systems you're least familiar with
            2. **Ask Questions** - Test your understanding with specific queries
            3. **Generate Questions** - Practice with USMLE-style questions
            4. **Use Flashcards** - Reinforce key concepts with spaced repetition
            5. **Track Progress** - Come back here to monitor your growth
            """)
        
        with col2:
            st.markdown("""
            #### 🔥 Quick Tips
            
            - **Daily Goal**: Review at least 2-3 systems per day
            - **Question Practice**: Aim for 10-15 questions daily
            - **Flashcards**: Review 20-30 cards per session
            - **Consistency**: Study regularly for best retention
            - **Active Recall**: Test yourself before checking answers
            """)
        
        st.markdown("---")
        
        # Feature usage guide
        st.markdown("### 🚀 Feature Guide")
        
        features = [
            {
                "Feature": "❓ Ask Question",
                "Purpose": "Get AI-powered answers to any medical question",
                "Best For": "Understanding complex concepts, clarifying doubts"
            },
            {
                "Feature": "📖 Medical Wiki",
                "Purpose": "Browse 370 comprehensive medical topics",
                "Best For": "Systematic learning, topic exploration"
            },
            {
                "Feature": "📝 Question Bank",
                "Purpose": "Generate USMLE-style practice questions",
                "Best For": "Exam preparation, self-assessment"
            },
            {
                "Feature": "🎴 Flashcards",
                "Purpose": "Study with interactive flashcards",
                "Best For": "Quick review, memorization, spaced repetition"
            },
            {
                "Feature": "📊 Analytics",
                "Purpose": "Track your learning progress",
                "Best For": "Monitoring improvement, identifying weak areas"
            }
        ]
        
        df_features = pd.DataFrame(features)
        st.dataframe(df_features, width="stretch", hide_index=True)
        
    except Exception as e:
        st.error(f"Error loading analytics: {str(e)}")
        st.info("Some statistics may be unavailable. Continue using the platform to build your analytics!")


def main():
    """Main application entry point"""
    init_session_state()
    
    # Check authentication
    if not check_authentication():
        show_login_page()
        return
    
    # Initialize system
    if not initialize_system():
        st.error("Failed to initialize system. Please refresh the page.")
        return
    
    # Initialize Gemini if API key is set
    if st.session_state.gemini_api_key and not st.session_state.qa_system:
        initialize_gemini()
    
    # Show appropriate page
    if st.session_state.current_page == "home":
        show_home_page()
    elif st.session_state.current_page == "qa":
        show_header()
        show_config_panel()
        show_qa_page()
    elif st.session_state.current_page == "wiki":
        show_header()
        show_config_panel()
        show_wiki_page()
    elif st.session_state.current_page == "question_bank":
        show_header()
        show_config_panel()
        show_question_bank_page()
    elif st.session_state.current_page == "flashcards":
        show_header()
        show_config_panel()
        show_flashcards_page()
    elif st.session_state.current_page == "analytics":
        show_header()
        show_config_panel()
        show_analytics_page()
    else:
        show_home_page()

if __name__ == "__main__":
    main()

