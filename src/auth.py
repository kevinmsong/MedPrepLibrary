"""
Authentication module for MedPrepLibrary
Handles user login and session management
"""
import streamlit as st
import hashlib
import sqlite3
from pathlib import Path
from datetime import datetime

class AuthManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()
        self.init_default_users()
    
    def init_database(self):
        """Initialize the user database"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.execute('PRAGMA journal_mode=WAL')  # Enable Write-Ahead Logging for better concurrency
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def init_default_users(self):
        """Initialize default users if they don't exist"""
        default_users = [
            ("ezhang", "medpassword"),
            ("kmsong", "medpassword")
        ]
        
        for username, password in default_users:
            self.create_user(username, password)
    
    def hash_password(self, password):
        """Hash a password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username, password):
        """Create a new user if they don't exist"""
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            cursor.execute(
                'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                (username, password_hash)
            )
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # User already exists
            if conn:
                conn.close()
            return False
        except Exception as e:
            if conn:
                conn.close()
            return False
    
    def verify_credentials(self, username, password):
        """Verify user credentials"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        cursor.execute(
            'SELECT user_id FROM users WHERE username = ? AND password_hash = ?',
            (username, password_hash)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            self.update_last_login(username)
            return True, result[0]
        return False, None
    
    def update_last_login(self, username):
        """Update the last login timestamp"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cursor = conn.cursor()
        
        cursor.execute(
            'UPDATE users SET last_login = ? WHERE username = ?',
            (datetime.now(), username)
        )
        
        conn.commit()
        conn.close()
    
    def get_user_id(self, username):
        """Get user ID by username"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cursor = conn.cursor()
        
        cursor.execute('SELECT user_id FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        
        conn.close()
        return result[0] if result else None


def show_login_page():
    """Display the login page"""
    st.markdown("""
        <style>
        .login-title {
            color: #2C5F7C;
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
            margin-top: 50px;
        }
        .login-subtitle {
            color: #666;
            text-align: center;
            margin-bottom: 40px;
            font-size: 1.1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<h1 class="login-title">🏥 MedPrepLibrary</h1>', unsafe_allow_html=True)
        st.markdown('<p class="login-subtitle">Your AI-Powered USMLE Step 1 Companion</p>', unsafe_allow_html=True)
        
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("🔐 Login", use_container_width=True, type="primary"):
            if username and password:
                # Initialize auth manager
                db_path = Path(__file__).parent.parent / "data" / "user_data" / "users.db"
                auth_manager = AuthManager(str(db_path))
                
                success, user_id = auth_manager.verify_credentials(username, password)
                
                if success:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.user_id = user_id
                    st.success(f"Welcome back, {username}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.warning("Please enter both username and password")


def check_authentication():
    """Check if user is authenticated"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    return st.session_state.authenticated


def logout():
    """Logout the current user"""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.user_id = None
    st.rerun()
