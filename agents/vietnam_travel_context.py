import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from agent_graph.tool_vietnam_travel_rag import lookup_vietnam_travel
import json


def vietnam_travel_context_lookup(state):
    """
    Look up relevant Vietnam travel context based on user preferences.
    Returns enriched state with context data and a flag indicating if more data is needed.
    """
    preferences = state.get('preferences', {})
    destination = preferences.get('destination', '')
    holiday_type = preferences.get('holiday_type', '')
    comments = preferences.get('comments', '')
    
    # Build search query based on preferences
    search_queries = []
    
    # Base destination query
    search_queries.append(f"Vietnam travel {holiday_type} {comments}".strip())
    
    # Add specific category searches based on holiday type
    if holiday_type.lower() in ['food', 'culture', 'family']:
        search_queries.append(f"Vietnam food culture {destination}")
    elif holiday_type.lower() in ['adventure', 'backpacking']:
        search_queries.append(f"Vietnam hidden gems adventure {destination}")
    elif holiday_type.lower() in ['party', 'festival']:
        search_queries.append(f"Vietnam festivals nightlife {destination}")
    else:
        search_queries.append(f"Vietnam local insights {destination}")
    
    # Collect context from RAG
    context_data = []
    total_context_length = 0
    
    for query in search_queries:
        try:
            context = lookup_vietnam_travel(query)
            if context and context.strip():
                context_data.append(context)
                total_context_length += len(context)
        except Exception as e:
            print(f"Error fetching context for query '{query}': {str(e)}")
    
    # Determine if we need more data (threshold can be adjusted)
    MIN_CONTEXT_LENGTH = 500  # Minimum characters for sufficient context
    needs_more_data = total_context_length < MIN_CONTEXT_LENGTH
    
    return {
        "vietnam_context": "\n\n".join(context_data),
        "context_data_sufficient": not needs_more_data,
        "context_length": total_context_length
    }