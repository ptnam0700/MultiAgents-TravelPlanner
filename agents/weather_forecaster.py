from langchain_core.messages import HumanMessage
from langchain_community.chat_models import ChatOllama
from llm_config import LLMConfig

# TODO: use weahter API to get real data
def weather_forecaster(state):
    llm = LLMConfig.get_openai_llm()
    
    prompt = f"""
        Based on the destination and travel dates, provide a detailed weather forecast including temperature, precipitation, and advice for travelers:
        Destination: {state['preferences'].get('destination', '')}
        Travel Dates: {state['preferences'].get('travel_dates', '')}
        Check-in Date: {state['preferences'].get('check_in_date', '')}
        Check-out Date: {state['preferences'].get('check_out_date', '')}
    """
    try:
        result = llm.invoke([HumanMessage(content=prompt)]).content
        return {"weather_forecast": result.strip()}
    except Exception as e:
        return {"weather_forecast": "", "warning": str(e)}