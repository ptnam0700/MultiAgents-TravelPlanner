#!/usr/bin/env python3

import sys
import os

# Test the workflow logic without Streamlit
sys.path.append('src')

from agents.vietnam_travel_context import vietnam_travel_context_lookup
from agents.conditional_tavily_search import conditional_tavily_search

def test_workflow():
    """Test the new Vietnam travel workflow nodes."""
    print("Testing Vietnam Travel Workflow...")
    
    # Test state
    test_state = {
        'preferences': {
            'destination': 'Hanoi',
            'holiday_type': 'any',
            'comments': 'interested in hidden gems and local food'
        }
    }
    
    print("\n1. Testing Vietnam Context Lookup...")
    try:
        context_result = vietnam_travel_context_lookup(test_state)
        print(f"Context data sufficient: {context_result.get('context_data_sufficient')}")
        print(f"Context length: {context_result.get('context_length')}")
        print(f"Context preview: {context_result.get('vietnam_context', '')[:200]}...")
        
        # Update state with context results
        test_state.update(context_result)
        
    except Exception as e:
        print(f"Context lookup error: {e}")
        # Set default values for testing conditional search
        test_state.update({
            'vietnam_context': '',
            'context_data_sufficient': False,
            'context_length': 0
        })
    
    print("\n2. Testing Conditional Tavily Search...")
    try:
        tavily_result = conditional_tavily_search(test_state)
        print(f"Tavily search performed: {tavily_result.get('tavily_search_performed')}")
        print(f"Results count: {tavily_result.get('tavily_results_count', 0)}")
        if tavily_result.get('tavily_search_results'):
            print(f"Search results preview: {tavily_result.get('tavily_search_results', '')[:200]}...")
    except Exception as e:
        print(f"Tavily search error: {e}")
    
    print("\n✅ Workflow test completed!")

if __name__ == "__main__":
    test_workflow()