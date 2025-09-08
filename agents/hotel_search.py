from langchain_core.messages import HumanMessage
from llm_config import LLMConfig
import json

def hotel_search(state):
    llm = LLMConfig.get_openai_llm()
    
    destination = state['preferences'].get('destination', '')
    budget_type = state['preferences'].get('budget_type', 'mid-range')
    check_in = state['preferences'].get('check_in_date', '')
    check_out = state['preferences'].get('check_out_date', '')
    guests = state['preferences'].get('guests', 1)
    
    prompt = f"""
    Search for hotel accommodations with the following requirements:
    
    Destination: {destination}
    Budget Type: {budget_type}
    Check-in Date: {check_in}
    Check-out Date: {check_out}
    Number of Guests: {guests}
    
    Please provide:
    1. Hotel recommendations with names, ratings, and approximate prices
    2. Location details and proximity to key attractions
    3. Amenities and features for each hotel
    4. Price ranges based on the specified budget type
    5. Booking tips and best practices
    
    Format the response clearly with hotel names as headers and details below each.
    Include price estimates in local currency and USD if applicable.
    """
    
    try:
        result = llm.invoke([HumanMessage(content=prompt)]).content
        return {"hotel_recommendations": result.strip()}
    except Exception as e:
        return {"hotel_recommendations": "", "warning": str(e)}