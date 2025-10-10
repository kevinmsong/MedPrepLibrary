"""
Flashcard manager with spaced repetition
"""

class FlashcardManager:
    def __init__(self, db_manager, rag_processor, gemini_qa):
        self.db = db_manager
        self.rag = rag_processor
        self.gemini = gemini_qa
    
    def generate_flashcards_for_topic(self, topic, system, count=10):
        """Generate flashcards for a specific topic"""
        generated_cards = []
        
        # Get relevant context
        context, sources = self.rag.get_context_for_query(topic, max_chunks=5)
        
        if not context:
            return []
        
        # Split context into smaller chunks for individual flashcards
        chunks = context.split('\n\n')
        
        for i, chunk in enumerate(chunks[:count]):
            if len(chunk.strip()) < 50:  # Skip very short chunks
                continue
            
            flashcard_data = self.gemini.generate_flashcard(
                context=chunk,
                topic=topic
            )
            
            if flashcard_data and 'front' in flashcard_data and 'back' in flashcard_data:
                # Add to database
                card_id = self.db.add_flashcard(
                    front_text=flashcard_data['front'],
                    back_text=flashcard_data['back'],
                    topic=topic,
                    system=system,
                    source_document=", ".join(sources)
                )
                
                flashcard_data['card_id'] = card_id
                generated_cards.append(flashcard_data)
        
        return generated_cards
    
    def get_due_cards(self, user_id, limit=20):
        """Get flashcards due for review"""
        return self.db.get_due_flashcards(user_id, limit)
    
    def record_review(self, user_id, card_id, quality):
        """Record a flashcard review
        quality mapping:
        - 0: Again (complete blackout)
        - 1: Hard (incorrect but remembered after seeing answer)
        - 3: Good (correct with some effort)
        - 5: Easy (perfect recall)
        """
        self.db.update_flashcard_progress(user_id, card_id, quality)
