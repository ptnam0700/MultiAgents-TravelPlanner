from langchain_community.tools.tavily_search import TavilySearchResults
import json


def conditional_tavily_search(state):
    """
    Conditionally search for additional Vietnam travel information using Tavily
    if the context data from RAG is insufficient.
    """
    # Check if we need more data
    # context_sufficient = state.get('context_data_sufficient', False)
    
    # if context_sufficient:
    #     # Skip Tavily search if we have sufficient context
    #     return {
    #         "tavily_search_results": "",
    #         "tavily_search_performed": False
    #     }
    
    # Perform Tavily search for hidden gems and food information
    preferences = state.get('preferences', {})
    destination = preferences.get('destination', '')
    holiday_type = preferences.get('holiday_type', '')
    comments = preferences.get('comments', '')
    
    tavily_tool = TavilySearchResults(max_results=5)
    
    search_results = []
    search_queries = []
    
    # Build search queries for hidden gems and food
    search_queries = [
        f"{destination} hidden gems {holiday_type} {comments}".strip(),
        f"{destination} local food culture {destination}".strip(),
        f"{destination} off the beaten path attractions {destination}".strip()
    ]
    
    # Perform searches
    for query in search_queries:
        try:
            results = tavily_tool.invoke({"query": query})
            if results:
                search_results.extend(results)
        except Exception as e:
            print(f"Error in Tavily search for query '{query}': {str(e)}")
    
    # Format results for context
    formatted_results = []
    for result in search_results:
        if isinstance(result, dict):
            title = result.get('title', 'No title')
            content = result.get('content', '')
            url = result.get('url', '')
            formatted_results.append(f"**{title}**\n{content}\nSource: {url}\n")
    
    return {
        "tavily_search_results": "\n".join(formatted_results),
        "tavily_search_performed": True,
        "tavily_results_count": len(search_results)
    }