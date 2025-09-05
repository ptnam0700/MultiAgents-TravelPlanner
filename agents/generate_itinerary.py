from langchain_core.messages import HumanMessage
import json 
from llm_config import LLMConfig

def generate_itinerary(state):
    llm = LLMConfig.get_openai_llm()

    # Combine all available context
    context_parts = []
    
    # Add Vietnam context from RAG
    vietnam_context = state.get('vietnam_context', '')
    if vietnam_context:
        context_parts.append(f"Vietnam Travel Context (Local Knowledge):\n{vietnam_context}")
    
    # Add Tavily search results if available
    tavily_results = state.get('tavily_search_results', '')
    if tavily_results:
        context_parts.append(f"Additional Travel Information (Web Search):\n{tavily_results}")
    
    # Add weather forecast if available
    weather_forecast = state.get('weather_forecast', '')
    if weather_forecast:
        context_parts.append(f"Weather Information:\n{weather_forecast}")
    
    combined_context = "\n\n".join(context_parts)

    prompt = f"""
        Using the following preferences and available context, create a detailed itinerary:
        
        PREFERENCES:
        {json.dumps(state['preferences'], indent=2)}
        
        AVAILABLE CONTEXT:
        {combined_context}

        Create a detailed itinerary that incorporates the local knowledge and context provided above.
        Include sections for each day, dining options, hidden gems, local food recommendations, and downtime.
        Make sure to reference specific places, foods, or activities mentioned in the context when relevant.
        """
    
    try:
        result = llm.invoke([HumanMessage(content=prompt)]).content
        return {"itinerary": result.strip()}
    except Exception as e:
        return {"itinerary": "", "warning": str(e)}