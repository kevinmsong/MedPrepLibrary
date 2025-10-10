"""
Gemini API integration for medical question answering
"""
import google.generativeai as genai

class GeminiQA:
    def __init__(self, api_key: str):
        if not api_key or not api_key.strip():
            raise ValueError("API key cannot be empty.")
        
        # Validate API key format (Gemini keys start with "AIza")
        api_key = api_key.strip()
        if not api_key.startswith("AIza"):
            raise ValueError("Invalid API key format. Gemini API keys should start with 'AIza'")
        
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.5-pro')
            self.api_key = api_key
            
            # Test the API key with a simple request
            try:
                test_response = self.model.generate_content("Test")
                # If we get here without exception, the key is valid
            except Exception as test_error:
                # Check if it's an API key error or something else
                error_msg = str(test_error).lower()
                if "api key" in error_msg or "invalid" in error_msg or "authentication" in error_msg:
                    raise ValueError(f"Invalid API key: {str(test_error)}")
                # Otherwise, key might be valid but other issue - allow it
                pass
                
        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"Failed to initialize Gemini API: {str(e)}")
    
    def get_answer(self, question: str, context: str) -> str:
        """Get an answer from Gemini API using the provided context"""
        prompt = f"""You are an expert medical educator specializing in USMLE Step 1 preparation. 
Answer the following question using ONLY the information provided in the context below from First Aid for the USMLE Step 1.

CRITICAL RULES:
- You MUST base your answer EXCLUSIVELY on the provided context
- DO NOT use external knowledge or synthesize information not in the context
- If the context does not contain enough information to fully answer the question, clearly state: "Based on the provided context from First Aid, [provide what IS available], however additional information would be needed for a complete answer."
- Always cite that your answer is based on the provided medical textbook context
- Structure your answer clearly with relevant sections
- Include all relevant details from the context

Context from First Aid for the USMLE Step 1:
{context}

Question:
{question}

Answer (based strictly on the provided context):"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error: Unable to get response from Gemini API - {str(e)}"
    
    def generate_question(self, context: str, topic: str, system: str, difficulty: str = "medium") -> dict:
        """Generate a USMLE-style multiple choice question from context"""
        
        difficulty_guidelines = {
            "easy": "Focus on basic recall and recognition of key concepts",
            "medium": "Require application of concepts to clinical scenarios",
            "hard": "Involve complex integration of multiple concepts and clinical reasoning"
        }
        
        prompt = f"""You are an expert USMLE Step 1 question writer. Generate a high-quality, clinically-oriented multiple choice question based on the provided context.

Topic: {topic}
System: {system}
Difficulty: {difficulty}
Guideline: {difficulty_guidelines.get(difficulty, difficulty_guidelines["medium"])}

Context:
{context}

Generate a question in the following JSON format:
{{
    "question_text": "A clinical vignette or direct question (2-4 sentences)",
    "options": {{
        "A": "First option",
        "B": "Second option",
        "C": "Third option",
        "D": "Fourth option",
        "E": "Fifth option"
    }},
    "correct_answer": "The letter of the correct answer (A-E)",
    "explanation": "Detailed explanation of why the correct answer is right and why other options are wrong (3-5 sentences)"
}}

Requirements:
- Make the question clinically relevant and realistic
- Ensure there is only ONE clearly correct answer
- Make distractors plausible but distinctly incorrect
- Base all content strictly on the provided context
- Use proper medical terminology
- Format as valid JSON

Generate the question now:"""
        
        try:
            response = self.model.generate_content(prompt)
            # Extract JSON from response
            import json
            import re
            
            text = response.text
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                question_data = json.loads(json_match.group())
                return question_data
            else:
                # If no JSON found, return error
                return None
        except Exception as e:
            print(f"Error generating question: {str(e)}")
            return None
    
    def generate_flashcard(self, context: str, topic: str) -> dict:
        """Generate a flashcard from context"""
        prompt = f"""You are creating a medical education flashcard for USMLE Step 1 preparation.

Topic: {topic}

Context:
{context}

Generate a flashcard in the following JSON format:
{{
    "front": "A clear, concise question or prompt (1-2 sentences)",
    "back": "A comprehensive answer with key details (2-4 sentences)"
}}

Requirements:
- Front should test understanding of a key concept
- Back should provide a complete, memorable answer
- Focus on high-yield information
- Use clear, precise medical terminology
- Base content strictly on the provided context

Generate the flashcard now:"""
        
        try:
            response = self.model.generate_content(prompt)
            import json
            import re
            
            text = response.text
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                flashcard_data = json.loads(json_match.group())
                return flashcard_data
            else:
                return None
        except Exception as e:
            print(f"Error generating flashcard: {str(e)}")
            return None
