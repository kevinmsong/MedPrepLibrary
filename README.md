# 🏥 MedPrepLibrary

**Your AI-Powered USMLE Step 1 Preparation Companion**

MedPrepLibrary is a comprehensive, document-faithful medical education platform designed for clinicians and trainees preparing for USMLE Step 1. Built with cutting-edge AI technology, it combines traditional study methods with intelligent features to maximize exam preparation efficiency.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.32.0-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### 🤖 AI-Powered Question Answering
- Ask any medical question and receive comprehensive, document-faithful answers
- Powered by Google's Gemini 2.0 Flash AI model
- Retrieval-Augmented Generation (RAG) ensures accuracy with source citations
- Context-aware responses from authoritative medical textbooks

### 📝 AI-Generated Question Bank
- USMLE-style multiple choice questions generated from your study materials
- Practice in random mix or system-based modes
- Timed practice blocks (40 questions) simulating real exam conditions
- Detailed explanations for correct and incorrect answers
- Performance tracking and analytics

### 🎴 Spaced Repetition Flashcards
- AI-generated flashcards from key medical concepts
- Intelligent spaced repetition algorithm (SM-2) for optimal retention
- Custom deck creation by topic and system
- Progress tracking and review scheduling

### 📖 Document-Adherent Wiki
- Comprehensive medical wiki organized by systems and topics
- Cross-linked pages for easy navigation
- Full-text search functionality
- Direct citations to source documents

### 📊 Progress Analytics
- Comprehensive performance tracking
- System-by-system accuracy breakdown
- Weak area identification with personalized recommendations
- Visual charts and detailed statistics

### 👥 Multi-User Support
- Individual user accounts with separate progress tracking
- Secure password authentication
- Personalized dashboards and study history

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/MedPrepLibrary.git
   cd MedPrepLibrary
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your medical textbooks**
   - Place your PDF files in the `data/pdfs/` directory
   - Supported: First Aid for USMLE Step 1 (2024, 2025) and other medical textbooks

4. **Run preprocessing** (first time only)
   ```bash
   python preprocess.py
   ```
   This will:
   - Extract text from PDFs
   - Generate semantic chunks
   - Create embeddings
   - Build FAISS index for efficient retrieval

5. **Launch the application**
   ```bash
   streamlit run app.py
   ```

6. **Access the app**
   - Open your browser to `http://localhost:8501`
   - Login with demo credentials:
     - Username: `ezhang` | Password: `medpassword`
     - Username: `kmsong` | Password: `medpassword`

7. **Enter your Gemini API key**
   - In the sidebar, enter your API key to unlock AI features
   - Get your free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

## 📁 Project Structure

```
MedPrepLibrary/
├── app.py                          # Main Streamlit application
├── preprocess.py                   # Document preprocessing script
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .streamlit/
│   └── config.toml                 # Streamlit configuration
├── data/
│   ├── pdfs/                       # Source PDF documents
│   ├── cache/                      # Processed documents & embeddings
│   └── user_data/                  # User progress databases
├── src/
│   ├── auth.py                     # Authentication system
│   ├── wiki/
│   │   └── wiki_builder.py         # Wiki generation
│   ├── qa_system/
│   │   ├── rag_processor.py        # RAG implementation
│   │   └── gemini_qa.py            # Gemini API integration
│   ├── question_bank/
│   │   └── question_manager.py     # Question generation & management
│   ├── flashcards/
│   │   └── flashcard_manager.py    # Flashcard system with SR
│   ├── analytics/
│   │   └── tracker.py              # Progress tracking
│   └── utils/
│       ├── database.py             # Database operations
│       ├── pdf_processor.py        # PDF text extraction
│       └── embeddings.py           # Embedding generation
└── assets/
    └── images/                     # UI assets
```

## 🎯 Usage Guide

### Dashboard
- View your overall statistics and performance metrics
- Get personalized study recommendations
- Quick access to all features

### Ask a Question
- Enter any medical question in natural language
- Receive comprehensive answers with source citations
- Save important answers for later review

### Wiki Browser
- Search for specific medical topics
- Browse by system (Cardiovascular, Respiratory, etc.)
- Read detailed, document-faithful content

### Question Bank
- **Random Mix**: Practice questions from all systems
- **System-Based**: Focus on specific systems
- **Timed Mode**: Simulate real exam conditions with 40-question blocks
- Review detailed explanations after each question

### Flashcards
- Review due cards using spaced repetition
- Generate new flashcards for any topic
- Rate your recall (Again, Hard, Good, Easy)
- Automatic scheduling for optimal retention

### Progress Analytics
- Track questions answered and accuracy
- View performance breakdown by system
- Identify weak areas needing improvement
- Monitor your study progress over time

## 🔧 Configuration

### Gemini API Key
The application requires a Gemini API key for AI features:
1. Get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Enter it in the sidebar of the application
3. The key is stored in your session (not persisted)

### Adding New Users
Edit `src/auth.py` to add new users:
```python
default_users = [
    ("username", "password"),
    # Add more users here
]
```

### Customizing Systems
Edit the `systems` list in relevant modules to add/remove medical systems.

## 🌐 Deployment on Streamlit Cloud

### Step 1: Prepare Your Repository

1. **Create a `.gitignore` file**
   ```
   data/pdfs/*.pdf
   data/cache/*
   data/user_data/*.db
   __pycache__/
   *.pyc
   .DS_Store
   ```

2. **Commit and push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository, branch, and `app.py`
5. Click "Deploy"

### Step 3: Add Secrets (Optional)

If you want to pre-configure the Gemini API key:
1. In Streamlit Cloud, go to App Settings → Secrets
2. Add:
   ```toml
   GEMINI_API_KEY = "your-api-key-here"
   ```

### Step 4: Upload PDFs

Since PDFs are large and copyrighted, you'll need to:
1. Deploy the app without PDFs initially
2. Use the app's interface to upload PDFs (if you add upload functionality)
3. Or manually add PDFs to the deployment (requires Streamlit Teams plan)

**Note**: For public deployment, ensure you have the legal right to use and distribute the PDF content.

## 📊 Technical Details

### RAG System
- **Embedding Model**: all-MiniLM-L6-v2 (384 dimensions)
- **Vector Database**: FAISS with L2 distance
- **Chunking Strategy**: Semantic chunking with 800-token chunks and 100-token overlap
- **Retrieval**: Top-k similarity search (k=5 by default)

### AI Models
- **Question Answering**: Gemini 2.0 Flash Exp
- **Question Generation**: Gemini 2.0 Flash Exp
- **Flashcard Generation**: Gemini 2.0 Flash Exp

### Database
- **Type**: SQLite
- **Tables**: users, questions, user_responses, flashcards, flashcard_progress, wiki_pages
- **Location**: `data/user_data/medprep.db`

### Spaced Repetition
- **Algorithm**: SM-2 (SuperMemo 2)
- **Quality Scale**: 0-5 (Again, Hard, Good, Easy)
- **Interval Calculation**: Adaptive based on performance

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This application is designed as a study aid and should not replace professional medical education or clinical judgment. The content is derived from medical textbooks and may not reflect the most current medical knowledge. Always verify information with authoritative sources and consult with qualified medical professionals.

## 🙏 Acknowledgments

- First Aid for the USMLE Step 1 (McGraw-Hill Education)
- Google Gemini AI for powering the intelligent features
- Streamlit for the excellent web framework
- The medical education community for inspiration

## 📧 Support

For questions, issues, or suggestions:
- Open an issue on GitHub
- Contact: [your-email@example.com]

## 🔮 Roadmap

- [ ] Add support for more medical textbooks (Pathoma, Sketchy, etc.)
- [ ] Implement collaborative study groups
- [ ] Add offline mode for mobile app
- [ ] Integrate with Anki for flashcard export
- [ ] Add voice input for questions
- [ ] Implement advanced analytics with ML predictions
- [ ] Create mobile apps (iOS/Android)

---

**Made with ❤️ for medical students and trainees preparing for USMLE Step 1**

*Last updated: October 2025*
