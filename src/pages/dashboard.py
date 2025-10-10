"""
Professional Dashboard Page for MedPrepLibrary
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

def show_dashboard():
    """Display the professional main dashboard"""
    
    # Hero Section
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #1E5F8C 0%, #2ECC71 100%); border-radius: 15px; margin-bottom: 2rem; color: white;">
            <h1 style="color: white; margin: 0; font-size: 2.5rem;">🏥 Welcome to MedPrepLibrary</h1>
            <p style="color: rgba(255,255,255,0.9); font-size: 1.2rem; margin-top: 0.5rem;">Your AI-Powered USMLE Step 1 Companion</p>
            <p style="color: rgba(255,255,255,0.8); font-size: 1rem; margin-top: 0.5rem;">Hello, <strong>{}</strong>! Ready to ace your exam?</p>
        </div>
    """.format(st.session_state.username), unsafe_allow_html=True)
    
    # Get user statistics
    stats = st.session_state.progress_tracker.get_user_dashboard_stats(st.session_state.user_id)
    
    # Key Metrics Row
    st.markdown("### 📊 Your Performance at a Glance")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 12px; text-align: center; color: white; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.5rem;">📝 Questions</div>
                <div style="font-size: 2.5rem; font-weight: bold;">{stats['total_questions']}</div>
                <div style="font-size: 0.8rem; opacity: 0.8; margin-top: 0.5rem;">Answered</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #2ECC71 0%, #27AE60 100%); padding: 1.5rem; border-radius: 12px; text-align: center; color: white; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.5rem;">✅ Correct</div>
                <div style="font-size: 2.5rem; font-weight: bold;">{stats['correct_answers']}</div>
                <div style="font-size: 0.8rem; opacity: 0.8; margin-top: 0.5rem;">Answers</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        accuracy_color = "#2ECC71" if stats['overall_accuracy'] >= 70 else "#F39C12" if stats['overall_accuracy'] >= 50 else "#E74C3C"
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, {accuracy_color} 0%, {accuracy_color}dd 100%); padding: 1.5rem; border-radius: 12px; text-align: center; color: white; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.5rem;">🎯 Accuracy</div>
                <div style="font-size: 2.5rem; font-weight: bold;">{stats['overall_accuracy']}%</div>
                <div style="font-size: 0.8rem; opacity: 0.8; margin-top: 0.5rem;">Overall</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #3498DB 0%, #2980B9 100%); padding: 1.5rem; border-radius: 12px; text-align: center; color: white; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.5rem;">🎴 Flashcards</div>
                <div style="font-size: 2.5rem; font-weight: bold;">{stats.get('flashcards_reviewed', 0)}</div>
                <div style="font-size: 0.8rem; opacity: 0.8; margin-top: 0.5rem;">Reviewed</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Two Column Layout
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # Study Recommendations
        st.markdown("### 💡 Personalized Study Recommendations")
        recommendations = st.session_state.progress_tracker.get_study_recommendations(st.session_state.user_id)
        
        if recommendations:
            for i, rec in enumerate(recommendations[:3]):  # Show top 3
                icon = "⚠️" if rec.get('priority') == 'high' else "💡"
                color = "#FFF3CD" if rec.get('priority') == 'high' else "#D1ECF1"
                border_color = "#FFC107" if rec.get('priority') == 'high' else "#17A2B8"
                
                st.markdown(f"""
                    <div style="background-color: {color}; border-left: 4px solid {border_color}; padding: 1rem; border-radius: 8px; margin-bottom: 0.8rem;">
                        <strong>{icon} {rec['message']}</strong>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="background-color: #D4EDDA; border-left: 4px solid #28A745; padding: 1rem; border-radius: 8px;">
                    <strong>🎉 Great job! Keep practicing to maintain your progress.</strong>
                </div>
            """, unsafe_allow_html=True)
        
        # Quick Stats
        st.markdown("### 📈 Recent Activity")
        
        # Create a simple activity chart if there's data
        if stats['total_questions'] > 0:
            # Placeholder for activity visualization
            st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <p style="margin: 0; color: #666;">
                        📅 You've answered <strong>{stats['total_questions']}</strong> questions with 
                        <strong style="color: #2ECC71;">{stats['overall_accuracy']}%</strong> accuracy.
                    </p>
                    <p style="margin-top: 0.8rem; color: #666;">
                        🔥 Keep up the momentum! Consistent practice is key to USMLE success.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <p style="margin: 0; color: #666;">
                        🚀 <strong>Get started!</strong> Begin your USMLE preparation journey by exploring our features below.
                    </p>
                </div>
            """, unsafe_allow_html=True)
    
    with col_right:
        # Quick Actions Card
        st.markdown("### 🚀 Quick Actions")
        st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        """, unsafe_allow_html=True)
        
        if st.button("❓ Ask Question", use_container_width=True, type="primary"):
            st.session_state.current_page = "qa"
            st.rerun()
        
        if st.button("📝 Practice Questions", use_container_width=True):
            st.session_state.current_page = "questions"
            st.rerun()
        
        if st.button("🎴 Study Flashcards", use_container_width=True):
            st.session_state.current_page = "flashcards"
            st.rerun()
        
        if st.button("📖 Browse Wiki", use_container_width=True):
            st.session_state.current_page = "wiki"
            st.rerun()
        
        if st.button("📊 View Analytics", use_container_width=True):
            st.session_state.current_page = "analytics"
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Tips Card
        st.markdown("### 💡 Study Tips")
        st.markdown("""
            <div style="background: linear-gradient(135deg, #F093FB 0%, #F5576C 100%); padding: 1.5rem; border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                <p style="margin: 0; font-size: 0.9rem; line-height: 1.6;">
                    <strong>✨ Pro Tip:</strong><br>
                    Use spaced repetition with flashcards for optimal retention. Review difficult topics multiple times!
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # Feature Showcase
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🎯 Explore Our Features")
    
    feat1, feat2, feat3 = st.columns(3)
    
    with feat1:
        st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">🤖</div>
                <h4 style="color: #1E5F8C; margin: 0.5rem 0;">AI Q&A</h4>
                <p style="color: #666; font-size: 0.9rem; margin: 0;">Get instant answers powered by Gemini 2.5 Pro</p>
            </div>
        """, unsafe_allow_html=True)
    
    with feat2:
        st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">📚</div>
                <h4 style="color: #1E5F8C; margin: 0.5rem 0;">Medical Wiki</h4>
                <p style="color: #666; font-size: 0.9rem; margin: 0;">370+ comprehensive USMLE topics</p>
            </div>
        """, unsafe_allow_html=True)
    
    with feat3:
        st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">📊</div>
                <h4 style="color: #1E5F8C; margin: 0.5rem 0;">Smart Analytics</h4>
                <p style="color: #666; font-size: 0.9rem; margin: 0;">Track progress and identify weak areas</p>
            </div>
        """, unsafe_allow_html=True)
