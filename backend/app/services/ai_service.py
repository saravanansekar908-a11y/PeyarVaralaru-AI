"""
Backward compatibility layer for ai_service.
Redirects to history_ai and history_research.
"""
from app.services.history_ai import is_gemini_available
from app.services.history_research import ask_place_question

def ask_question(db, question: str, language: str = "ta") -> dict:
    return ask_place_question(db, question, language)

__all__ = ["is_gemini_available", "ask_question"]
