from langchain_core.messages import HumanMessage
from llm_config import LLMConfig 

def packing_list_generator(state):
    llm = LLMConfig.get_openai_llm()
    prompt = f"""
        Generate a comprehensive packing list for a {state['preferences'].get('holiday_type', 'general')} holiday in {state['preferences'].get('destination', '')} during {state['preferences'].get('travel_dates', '')}.
        Travel dates: {state['preferences'].get('check_in_date', '')} to {state['preferences'].get('check_out_date', '')}
        Include essentials based on expected weather and trip type.
    """
    try:
        result = llm.invoke([HumanMessage(content=prompt)]).content
        return {"packing_list": result.strip()}
    except Exception as e:
        return {"packing_list": "", "warning": str(e)}