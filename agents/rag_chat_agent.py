"""
RAG-enabled Chat Agent for Vietnam Travel Planning

This module provides a chat agent that combines travel itinerary context
with Vietnam-specific knowledge from a RAG (Retrieval-Augmented Generation) system.
"""

import sys
import os

# Add src to path for RAG system imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.chatbot.backend import ChatBot
from src.agent_graph.load_tools_config import LoadToolsConfig

# Initialize RAG system components
try:
    rag_config = LoadToolsConfig()
    rag_chatbot = ChatBot()
except Exception as e:
    print(f"Warning: RAG system initialization failed: {e}")
    rag_chatbot = None


def rag_chat_node(state):
    """
    RAG-enabled chat node that combines travel itinerary context with Vietnam travel knowledge.
    Uses AI tools to intelligently decide when to trigger itinerary updates.
    
    Args:
        state (dict): The current state containing user preferences, itinerary, and chat history
        
    Returns:
        dict: Updated state with chat response, updated chat history, and tool decisions
    """
    if not rag_chatbot:
        # Fallback to basic response if RAG system failed to initialize
        return {
            "chat_response": "I'm sorry, the enhanced chat system is currently unavailable. Please try again later.",
            "chat_history": state.get('chat_history', [])
        }
    
    try:
        # Extract travel context from state
        preferences = state.get('preferences', {})
        
        # Format the user question with comprehensive travel context
        context_message = f"""
            Travel Planning Context:
            - Destination: {preferences.get('destination', 'Vietnam')}
            - Travel Dates: {preferences.get('travel_dates', 'N/A')}
            - Check-in: {preferences.get('check_in_date', 'N/A')}
            - Check-out: {preferences.get('check_out_date', 'N/A')}
            - Number of People: {preferences.get('num_people', 'N/A')}
            - Travel Type: {preferences.get('holiday_type', 'Any')}
            - Budget: {preferences.get('budget_type', 'Mid-Range')}
            - Additional Comments: {preferences.get('comments', 'None')}

            Current Itinerary: {state.get('itinerary', 'Not generated yet')}

            User Question: {state.get('user_question', '')}

            You have access to tools to help with travel planning. Consider using:
            - `update_travel_itinerary` if the user wants changes to their itinerary
            - `analyze_itinerary_satisfaction` if you need to assess user satisfaction
            - `lookup_vietnam_travel` for Vietnam-specific information
            
            Analyze the user's request intelligently and use the appropriate tools when needed.
            Provide helpful travel advice, especially for Vietnam travel. Use your knowledge of Vietnam's 
            hidden gems, food culture, local insights, and practical travel tips.
        """
        
        # Get existing chat history in the format expected by RAG chatbot
        chat_history = []
        for entry in state.get('chat_history', []):
            chat_history.append({"role": "user", "content": entry["question"]})
            chat_history.append({"role": "assistant", "content": entry["response"]})
        
        # Get response from RAG chatbot with tools
        response = rag_chatbot.respond(chat_history, context_message)
        
        # Check if the response contains tool calls (this would be in the tool execution)
        # For now, we'll let the backend graph handle tool detection
        needs_update = False
        
        # Create new chat entry
        chat_entry = {
            "question": state.get('user_question', ''),
            "response": response
        }
        
        # Update chat history
        updated_history = state.get('chat_history', []) + [chat_entry]
        
        return {
            "chat_response": response,
            "chat_history": updated_history,
            "needs_itinerary_update": needs_update
        }
    
    except Exception as e:
        error_msg = f"Sorry, I encountered an error while processing your question: {str(e)}"
        chat_entry = {
            "question": state.get('user_question', ''),
            "response": error_msg
        }
        updated_history = state.get('chat_history', []) + [chat_entry]
        
        return {
            "chat_response": error_msg,
            "chat_history": updated_history,
            "needs_itinerary_update": False
        }


# For backwards compatibility, also expose the function directly
def chat_node(state):
    """Alias for rag_chat_node for backwards compatibility"""
    return rag_chat_node(state)