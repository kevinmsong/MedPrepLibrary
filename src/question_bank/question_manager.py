"""
Question bank manager for generating and managing practice questions
"""
import streamlit as st
from pathlib import Path
import random

class QuestionBankManager:
    def __init__(self, db_manager, rag_processor, gemini_qa):
        self.db = db_manager
        self.rag = rag_processor
        self.gemini = gemini_qa
        self.systems = [
            "Cardiovascular",
            "Respiratory",
            "Gastrointestinal",
            "Renal",
            "Endocrine",
            "Neurology",
            "Hematology",
            "Immunology",
            "Musculoskeletal",
            "Reproductive",
            "Pathology",
            "Pharmacology",
            "Microbiology",
            "Biochemistry",
            "Behavioral Science"
        ]
    
    def generate_questions_for_topic(self, topic, system, count=5, difficulty="medium"):
        """Generate questions for a specific topic"""
        generated_questions = []
        
        # Get relevant context for the topic
        context, sources = self.rag.get_context_for_query(topic, max_chunks=3)
        
        if not context:
            return []
        
        # Generate multiple questions
        for i in range(count):
            question_data = self.gemini.generate_question(
                context=context,
                topic=topic,
                system=system,
                difficulty=difficulty
            )
            
            if question_data:
                # Add to database
                question_id = self.db.add_question(
                    topic=topic,
                    system=system,
                    difficulty=difficulty,
                    question_text=question_data['question_text'],
                    options=question_data['options'],
                    correct_answer=question_data['correct_answer'],
                    explanation=question_data['explanation'],
                    source_document=", ".join(sources),
                    source_page=None
                )
                
                question_data['question_id'] = question_id
                generated_questions.append(question_data)
        
        return generated_questions
    
    def get_practice_set(self, mode="random", system=None, count=40):
        """Get a practice set of questions"""
        if mode == "random":
            return self.db.get_random_questions(count)
        elif mode == "system" and system:
            return self.db.get_questions_by_system(system, limit=count)
        else:
            return []
    
    def check_answer(self, user_id, question_id, selected_answer, correct_answer, time_taken=None):
        """Check if answer is correct and record response"""
        is_correct = (selected_answer == correct_answer)
        
        # Record the response
        self.db.record_user_response(
            user_id=user_id,
            question_id=question_id,
            selected_answer=selected_answer,
            is_correct=is_correct,
            time_taken=time_taken
        )
        
        return is_correct
