from langchain_core.messages import HumanMessage
import json 
from llm_config import LLMConfig

def generate_itinerary(state):
    llm = LLMConfig.get_openai_llm()

    prompt = f"""
        Using the following preferences, create a detailed itinerary:
        {json.dumps(state['preferences'], indent=2)}

        Include sections for each day, dining options, and downtime.
        """
    
    try:
        result = llm.invoke([HumanMessage(content=prompt)]).content
        return {"itinerary": result.strip()}
    except Exception as e:
        return {"itinerary": "", "warning": str(e)}