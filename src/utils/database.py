"""
Database utility module for MedPrepLibrary
Handles all database operations for user progress, questions, and flashcards
"""
import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_all_tables()
    
    def init_all_tables(self):
        """Initialize all database tables"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.execute('PRAGMA journal_mode=WAL')  # Enable Write-Ahead Logging
        cursor = conn.cursor()
        
        # Questions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                question_id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                system TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                question_text TEXT NOT NULL,
                options TEXT NOT NULL,
                correct_answer TEXT NOT NULL,
                explanation TEXT NOT NULL,
                source_document TEXT NOT NULL,
                source_page TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User responses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_responses (
                response_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                question_id INTEGER NOT NULL,
                selected_answer TEXT NOT NULL,
                is_correct INTEGER NOT NULL,
                time_taken INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (question_id) REFERENCES questions(question_id)
            )
        ''')
        
        # Flashcards table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS flashcards (
                card_id INTEGER PRIMARY KEY AUTOINCREMENT,
                front_text TEXT NOT NULL,
                back_text TEXT NOT NULL,
                topic TEXT NOT NULL,
                system TEXT NOT NULL,
                source_document TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Flashcard progress table (SM-2 algorithm)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS flashcard_progress (
                progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                card_id INTEGER NOT NULL,
                ease_factor REAL DEFAULT 2.5,
                interval INTEGER DEFAULT 1,
                repetitions INTEGER DEFAULT 0,
                next_review_date TIMESTAMP,
                last_reviewed TIMESTAMP,
                FOREIGN KEY (card_id) REFERENCES flashcards(card_id),
                UNIQUE(user_id, card_id)
            )
        ''')
        
        # Wiki pages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wiki_pages (
                page_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE NOT NULL,
                system TEXT NOT NULL,
                content TEXT NOT NULL,
                related_pages TEXT,
                source_documents TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User bookmarks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_bookmarks (
                bookmark_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                page_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (page_id) REFERENCES wiki_pages(page_id),
                UNIQUE(user_id, page_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # Question Bank Methods
    def add_question(self, topic, system, difficulty, question_text, options, 
                     correct_answer, explanation, source_document, source_page=None):
        """Add a new question to the database"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO questions (topic, system, difficulty, question_text, options, 
                                 correct_answer, explanation, source_document, source_page)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (topic, system, difficulty, question_text, json.dumps(options), 
              correct_answer, explanation, source_document, source_page))
        
        question_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return question_id
    
    def get_questions_by_system(self, system, limit=None):
        """Get questions filtered by system"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cursor = conn.cursor()
        
        query = 'SELECT * FROM questions WHERE system = ?'
        if limit:
            query += f' LIMIT {limit}'
        
        cursor.execute(query, (system,))
        questions = cursor.fetchall()
        conn.close()
        
        return self._format_questions(questions)
    
    def get_random_questions(self, count=40):
        """Get random questions for practice"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM questions ORDER BY RANDOM() LIMIT ?', (count,))
        questions = cursor.fetchall()
        conn.close()
        
        return self._format_questions(questions)
    
    def _format_questions(self, questions):
        """Format question tuples into dictionaries"""
        formatted = []
        for q in questions:
            formatted.append({
                'question_id': q[0],
                'topic': q[1],
                'system': q[2],
                'difficulty': q[3],
                'question_text': q[4],
                'options': json.loads(q[5]),
                'correct_answer': q[6],
                'explanation': q[7],
                'source_document': q[8],
                'source_page': q[9],
                'created_at': q[10]
            })
        return formatted
    
    def record_user_response(self, user_id, question_id, selected_answer, 
                            is_correct, time_taken=None):
        """Record a user's response to a question"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO user_responses (user_id, question_id, selected_answer, 
                                       is_correct, time_taken)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, question_id, selected_answer, int(is_correct), time_taken))
        
        conn.commit()
        conn.close()
    
    def get_user_statistics(self, user_id):
        """Get comprehensive statistics for a user"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cursor = conn.cursor()
        
        # Total questions answered
        cursor.execute('SELECT COUNT(*) FROM user_responses WHERE user_id = ?', (user_id,))
        total_questions = cursor.fetchone()[0]
        
        # Correct answers
        cursor.execute('SELECT COUNT(*) FROM user_responses WHERE user_id = ? AND is_correct = 1', (user_id,))
        correct_answers = cursor.fetchone()[0]
        
        # Performance by system
        cursor.execute('''
            SELECT q.system, 
                   COUNT(*) as total,
                   SUM(ur.is_correct) as correct
            FROM user_responses ur
            JOIN questions q ON ur.question_id = q.question_id
            WHERE ur.user_id = ?
            GROUP BY q.system
        ''', (user_id,))
        
        system_performance = {}
        for row in cursor.fetchall():
            system_performance[row[0]] = {
                'total': row[1],
                'correct': row[2],
                'accuracy': (row[2] / row[1] * 100) if row[1] > 0 else 0
            }
        
        conn.close()
        
        return {
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'accuracy': (correct_answers / total_questions * 100) if total_questions > 0 else 0,
            'system_performance': system_performance
        }
    
    # Flashcard Methods
    def add_flashcard(self, front_text, back_text, topic, system, source_document):
        """Add a new flashcard"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO flashcards (front_text, back_text, topic, system, source_document)
            VALUES (?, ?, ?, ?, ?)
        ''', (front_text, back_text, topic, system, source_document))
        
        card_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return card_id
    
    def get_due_flashcards(self, user_id, limit=20):
        """Get flashcards due for review using SM-2 algorithm"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cursor = conn.cursor()
        
        # Get cards that are due or new cards
        cursor.execute('''
            SELECT f.*, fp.ease_factor, fp.interval, fp.repetitions, 
                   fp.next_review_date, fp.last_reviewed
            FROM flashcards f
            LEFT JOIN flashcard_progress fp ON f.card_id = fp.card_id AND fp.user_id = ?
            WHERE fp.next_review_date IS NULL OR fp.next_review_date <= datetime('now')
            ORDER BY fp.next_review_date ASC
            LIMIT ?
        ''', (user_id, limit))
        
        cards = cursor.fetchall()
        conn.close()
        
        return self._format_flashcards(cards)
    
    def _format_flashcards(self, cards):
        """Format flashcard tuples into dictionaries"""
        formatted = []
        for c in cards:
            formatted.append({
                'card_id': c[0],
                'front_text': c[1],
                'back_text': c[2],
                'topic': c[3],
                'system': c[4],
                'source_document': c[5],
                'ease_factor': c[7] if len(c) > 7 else 2.5,
                'interval': c[8] if len(c) > 8 else 1,
                'repetitions': c[9] if len(c) > 9 else 0
            })
        return formatted
    
    def update_flashcard_progress(self, user_id, card_id, quality):
        """Update flashcard progress using SM-2 algorithm
        quality: 0-5 (0=complete blackout, 5=perfect response)
        """
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cursor = conn.cursor()
        
        # Get current progress
        cursor.execute('''
            SELECT ease_factor, interval, repetitions
            FROM flashcard_progress
            WHERE user_id = ? AND card_id = ?
        ''', (user_id, card_id))
        
        result = cursor.fetchone()
        
        if result:
            ease_factor, interval, repetitions = result
        else:
            ease_factor, interval, repetitions = 2.5, 1, 0
        
        # SM-2 algorithm
        if quality >= 3:
            if repetitions == 0:
                interval = 1
            elif repetitions == 1:
                interval = 6
            else:
                interval = int(interval * ease_factor)
            repetitions += 1
        else:
            repetitions = 0
            interval = 1
        
        ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        ease_factor = max(1.3, ease_factor)
        
        next_review_date = datetime.now() + timedelta(days=interval)
        
        # Update or insert progress
        cursor.execute('''
            INSERT OR REPLACE INTO flashcard_progress 
            (user_id, card_id, ease_factor, interval, repetitions, next_review_date, last_reviewed)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, card_id, ease_factor, interval, repetitions, next_review_date, datetime.now()))
        
        conn.commit()
        conn.close()
    
    # Wiki Methods
    def add_wiki_page(self, title, system, content, related_pages=None, source_documents=None):
        """Add a new wiki page"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO wiki_pages (title, system, content, related_pages, source_documents)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, system, content, 
                  json.dumps(related_pages) if related_pages else None,
                  json.dumps(source_documents) if source_documents else None))
            
            page_id = cursor.lastrowid
            conn.commit()
            return page_id
        except sqlite3.IntegrityError:
            # Page already exists, update it
            cursor.execute('''
                UPDATE wiki_pages 
                SET content = ?, related_pages = ?, source_documents = ?, updated_at = ?
                WHERE title = ?
            ''', (content, 
                  json.dumps(related_pages) if related_pages else None,
                  json.dumps(source_documents) if source_documents else None,
                  datetime.now(), title))
            conn.commit()
            
            cursor.execute('SELECT page_id FROM wiki_pages WHERE title = ?', (title,))
            return cursor.fetchone()[0]
        finally:
            conn.close()
    
    def get_wiki_page(self, title):
        """Get a wiki page by title"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM wiki_pages WHERE title = ?', (title,))
        page = cursor.fetchone()
        conn.close()
        
        if page:
            return {
                'page_id': page[0],
                'title': page[1],
                'system': page[2],
                'content': page[3],
                'related_pages': json.loads(page[4]) if page[4] else [],
                'source_documents': json.loads(page[5]) if page[5] else [],
                'created_at': page[6],
                'updated_at': page[7]
            }
        return None
    
    def search_wiki_pages(self, query):
        """Search wiki pages by title or content"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT page_id, title, system 
            FROM wiki_pages 
            WHERE title LIKE ? OR content LIKE ?
            LIMIT 50
        ''', (f'%{query}%', f'%{query}%'))
        
        results = cursor.fetchall()
        conn.close()
        
        return [{'page_id': r[0], 'title': r[1], 'system': r[2]} for r in results]
    
    def get_all_wiki_pages_by_system(self):
        """Get all wiki pages organized by system"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cursor = conn.cursor()
        
        cursor.execute('SELECT page_id, title, system FROM wiki_pages ORDER BY system, title')
        pages = cursor.fetchall()
        conn.close()
        
        # Organize by system
        by_system = {}
        for page in pages:
            system = page[2]
            if system not in by_system:
                by_system[system] = []
            by_system[system].append({'page_id': page[0], 'title': page[1]})
        
        return by_system
