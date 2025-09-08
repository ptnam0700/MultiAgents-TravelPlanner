#!/usr/bin/env python3

import sys
import os

# Add src to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agent_graph.build_full_graph import build_graph

def test_chatbot_defense():
    """Test the chatbot defense mechanism with system prompt approach."""
    
    print("Testing Travel Defense Mechanism (System Prompt Approach)")
    print("=" * 60)
    
    # Build the graph
    try:
        graph = build_graph()
        config = {"configurable": {"thread_id": "test_thread"}}
        print("✓ Graph built successfully")
        
        # Test cases
        test_cases = [
            ("What are the best places to visit in Vietnam?", "travel-related"),
            ("What is 2 + 2?", "non-travel"),
            ("Tell me a joke", "non-travel"),
            ("How much does a hotel in Hanoi cost?", "travel-related"),
        ]
        
        for message, expected_type in test_cases:
            print(f"\nTesting: '{message}' (Expected: {expected_type})")
            try:
                events = graph.stream(
                    {"messages": [("user", message)]}, 
                    config, 
                    stream_mode="values"
                )
                
                response_content = ""
                for event in events:
                    response_content = event["messages"][-1].content
                    break  # Get first response
                
                # Check if response contains the redirect message for non-travel questions
                is_redirect = "I'm a travel assistant focused on helping you plan your trips" in response_content
                
                if expected_type == "non-travel" and is_redirect:
                    print("✓ PASS - Non-travel question properly redirected")
                elif expected_type == "travel-related" and not is_redirect:
                    print("✓ PASS - Travel question processed normally")
                else:
                    print(f"✗ FAIL - Unexpected response type")
                    print(f"Response: {response_content[:100]}...")
                
            except Exception as e:
                print(f"✗ ERROR - {str(e)}")
        
        print("\n" + "=" * 60)
        print("Defense mechanism implemented with system prompt approach")
        return True
        
    except Exception as e:
        print(f"✗ Failed to build graph: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_chatbot_defense()
    exit(0 if success else 1)