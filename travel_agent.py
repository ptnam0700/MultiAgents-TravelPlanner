import streamlit as st
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

from langchain_community.utilities import GoogleSerperAPIWrapper
from dotenv import load_dotenv
import os
from agents import generate_itinerary, recommend_activities, fetch_useful_links, weather_forecaster, packing_list_generator, food_culture_recommender, rag_chat_agent, hotel_search, vietnam_travel_context, conditional_tavily_search
from utils_export import export_to_pdf

# Load environment variables
load_dotenv()

# Initialize LLM
st.set_page_config(page_title="SaturdAI - Vietnam Travel Planner", layout="wide")
try:
    llm = ChatOpenAI(
        model="gpt-4o-mini", 
        api_key=os.getenv("OPENAI_GPT4_API_KEY"),
        base_url=os.getenv("HOST_JPE"),
    )
except Exception as e:
    st.error(f"LLM initialization failed: {str(e)}")
    st.stop()

# Initialize GoogleSerperAPIWrapper
try:
    search = GoogleSerperAPIWrapper()
except Exception as e:
    st.error(f"Serper API initialization failed: {str(e)}")
    st.stop()

# Define state
class GraphState(TypedDict):
    preferences_text: str
    preferences: dict
    itinerary: str
    activity_suggestions: str
    useful_links: list[dict]
    weather_forecast: str
    packing_list: str
    food_culture_info: str
    hotel_recommendations: str
    chat_history: Annotated[list[dict], "List of question-response pairs"]
    user_question: str
    chat_response: str
    vietnam_context: str
    context_data_sufficient: bool
    context_length: int
    tavily_search_results: str
    tavily_search_performed: bool
    tavily_results_count: int

# ------------------- LangGraph -------------------

workflow = StateGraph(GraphState)

# Add nodes in the new workflow order
workflow.add_node("vietnam_context_lookup", vietnam_travel_context.vietnam_travel_context_lookup)
workflow.add_node("conditional_tavily_search", conditional_tavily_search.conditional_tavily_search)
workflow.add_node("weather_forecaster", weather_forecaster.weather_forecaster)
workflow.add_node("generate_itinerary", generate_itinerary.generate_itinerary)

# Define the workflow: context -> conditional search -> weather -> itinerary
workflow.set_entry_point("vietnam_context_lookup")
workflow.add_edge("vietnam_context_lookup", "conditional_tavily_search")
workflow.add_edge("conditional_tavily_search", "weather_forecaster")
workflow.add_edge("weather_forecaster", "generate_itinerary")
workflow.add_edge("generate_itinerary", END)

graph = workflow.compile()

# ------------------- UI -------------------

st.markdown("# SaturdAI - Vietnam Travel Planner")

if "state" not in st.session_state:
    st.session_state.state = {
        "preferences_text": "",
        "preferences": {},
        "itinerary": "",
        "activity_suggestions": "",
        "useful_links": [],
        "weather_forecast": "",
        "packing_list": "",
        "food_culture_info": "",
        "hotel_recommendations": "",
        "chat_history": [],
        "user_question": "",
        "chat_response": "",
        "vietnam_context": "",
        "context_data_sufficient": False,
        "context_length": 0,
        "tavily_search_results": "",
        "tavily_search_performed": False,
        "tavily_results_count": 0
    }

with st.form("travel_form"):
    col1, col2 = st.columns(2)
    with col1:
        destination = st.text_input("Destination")
        num_people = st.selectbox("Number of People", ["1", "2", "3", "4-6", "7-10", "10+"])
        date_range = st.date_input("Travel Dates", value=[], key="date_range")
    with col2:
        holiday_type = st.selectbox("Holiday Type", ["Any", "Party", "Skiing", "Backpacking", "Family", "Beach", "Festival", "Adventure", "City Break", "Romantic", "Cruise"])
        budget_type = st.selectbox("Budget Type", ["Budget", "Mid-Range", "Luxury", "Backpacker", "Family"])
        comments = st.text_area("Additional Comments")
    submit_btn = st.form_submit_button("Generate Itinerary")

if submit_btn:
    check_in_date = date_range[0] if date_range and len(date_range) > 0 else None
    check_out_date = date_range[1] if date_range and len(date_range) > 1 else None
    
    preferences_text = f"Destination: {destination}\nPeople: {num_people}\nType: {holiday_type}\nBudget: {budget_type}\nTravel Dates: {date_range if date_range else 'Not specified'}\nComments: {comments}"
    preferences = {
        "destination": destination,
        "num_people": num_people,
        "holiday_type": holiday_type,
        "budget_type": budget_type,
        "check_in_date": str(check_in_date) if check_in_date else "",
        "check_out_date": str(check_out_date) if check_out_date else "",
        "guests": num_people,
        "travel_dates": str(date_range) if date_range else "",
        "comments": comments
    }
    st.session_state.state.update({
        "preferences_text": preferences_text,
        "preferences": preferences,
        "chat_history": [],
        "user_question": "",
        "chat_response": "",
        "activity_suggestions": "",
        "useful_links": [],
        "weather_forecast": "",
        "packing_list": "",
        "food_culture_info": "",
        "hotel_recommendations": "",
        "vietnam_context": "",
        "context_data_sufficient": False,
        "context_length": 0,
        "tavily_search_results": "",
        "tavily_search_performed": False,
        "tavily_results_count": 0
    })
    with st.spinner("Generating itinerary..."):
        result = graph.invoke(st.session_state.state)
        st.session_state.state.update(result)
        if result.get("itinerary"):
            st.success("Itinerary Created")
        else:
            st.error("Failed to generate itinerary.")

# Layout
if st.session_state.state.get("itinerary"):
    col_itin, col_chat = st.columns([3, 2])

    with col_itin:
        st.markdown("### Travel Itinerary")
        st.markdown(st.session_state.state["itinerary"])

        # All agent buttons in one row
        col_btn1, col_btn2, col_btn3, col_btn4, col_btn5, col_btn6 = st.columns(6)
        with col_btn1:
            if st.button("Get Activity Suggestions"):
                with st.spinner("Fetching activity suggestions..."):
                    result = recommend_activities.recommend_activities(st.session_state.state)
                    st.session_state.state.update(result)
        with col_btn2:
            if st.button("Get Useful Links"):
                with st.spinner("Fetching useful links..."):
                    result = fetch_useful_links.fetch_useful_links(st.session_state.state)
                    st.session_state.state.update(result)
        with col_btn3:
            if st.button("Get Weather Forecast"):
                with st.spinner("Fetching weather forecast..."):
                    result = weather_forecaster.weather_forecaster(st.session_state.state)
                    st.session_state.state.update(result)
        with col_btn4:
            if st.button("Get Packing List"):
                with st.spinner("Generating packing list..."):
                    result = packing_list_generator.packing_list_generator(st.session_state.state)
                    st.session_state.state.update(result)
        with col_btn5:
            if st.button("🍽️ Food & Culture", key="food"):
                with st.spinner("Fetching food and culture info..."):
                    result = food_culture_recommender.food_culture_recommender(st.session_state.state)
                    st.session_state.state.update(result)
        with col_btn6:
            if st.button("🏨 Hotels", key="hotels"):
                with st.spinner("Searching for hotels..."):
                    result = hotel_search.hotel_search(st.session_state.state)
                    st.session_state.state.update(result)

        # Display all agent outputs in expanders
        if st.session_state.state.get("activity_suggestions"):
            with st.expander("🎯 Activity Suggestions", expanded=False):
                st.markdown(st.session_state.state["activity_suggestions"])

        if st.session_state.state.get("useful_links"):
            with st.expander("🔗 Useful Links", expanded=False):
                for link in st.session_state.state["useful_links"]:
                    st.markdown(f"- [{link['title']}]({link['link']})")

        if st.session_state.state.get("weather_forecast"):
            with st.expander("🌤️ Weather Forecast", expanded=False):
                st.markdown(st.session_state.state["weather_forecast"])

        if st.session_state.state.get("packing_list"):
            with st.expander("🎒 Packing List", expanded=False):
                st.markdown(st.session_state.state["packing_list"])

        if st.session_state.state.get("food_culture_info"):
            with st.expander("🍽️ Food & Culture Info", expanded=False):
                st.markdown(st.session_state.state["food_culture_info"])

        if st.session_state.state.get("hotel_recommendations"):
            with st.expander("🏨 Hotel Recommendations", expanded=False):
                st.markdown(st.session_state.state["hotel_recommendations"])

        # Export PDF button
        if st.button("Export as PDF"):
            pdf_path = export_to_pdf(st.session_state.state["itinerary"])
            if pdf_path:
                with open(pdf_path, "rb") as f:
                    st.download_button("Download Itinerary PDF", f, file_name="itinerary.pdf")

    with col_chat:
        st.markdown("### Chat About Your Itinerary")
        for chat in st.session_state.state["chat_history"]:
            with st.chat_message("user"):
                st.markdown(chat["question"])
            with st.chat_message("assistant"):
                st.markdown(chat["response"])

        if user_input := st.chat_input("Ask something about your itinerary"):
            st.session_state.state["user_question"] = user_input
            with st.spinner("Generating response..."):
                result = rag_chat_agent.chat_node(st.session_state.state)
                st.session_state.state.update(result)
                st.rerun()
else:
    st.info("Fill the form and generate an itinerary to begin.")