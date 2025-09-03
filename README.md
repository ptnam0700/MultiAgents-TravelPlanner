# MultiAgents-with-Langgraph-TravelItineraryPlanner

Welcome to the **AI Travel Itinerary Planner**, a modular multi-agent system built with Streamlit, LangGraph, and Ollama. This application leverages multiple AI agents to generate personalized travel itineraries and provide additional travel-related insights based on user preferences. The system is designed for modularity, with agents split into individual scripts for maintainability and scalability.

- **Repository**: [https://github.com/vikrambhat2/MultiAgents-with-Langgraph-TravelItineraryPlanner](https://github.com/vikrambhat2/MultiAgents-with-Langgraph-TravelItineraryPlanner)


## Overview

The Vietnam Travel Planner uses a LangGraph workflow to manage a set of agents that collaboratively process user inputs (e.g., destination, month, duration) to produce a detailed itinerary, activity suggestions, weather forecasts, packing lists, food/culture recommendations, useful links, and a chat interface. 

**🌟 NEW: ChromaDB Vector Database Integration**
The system now includes a ChromaDB vector database populated with hidden Vietnamese travel gems, local knowledge, and niche information from articles and blogs. This enables authentic, local recommendations that go beyond typical tourist guides.

The system integrates with OpenAI API (chatGPT-o4-mini model) and the Google Serper API for web searches, enhanced with local Vietnamese travel knowledge through semantic search.

## Features
- Generate a detailed travel itinerary with daily plans, dining options, and downtime.
- Suggest unique local activities based on the itinerary and preferences.
- Fetch the top 5 travel guide links for the destination and month.
- Provide weather forecasts, packing lists, and food/culture recommendations.
- Offer a conversational chat to answer itinerary-related questions.
- Export the itinerary as a PDF.

## Directory Structure

```
MultiAgents-with-CrewAI-TravelItineraryPlanner/
│
├── agents/
│   ├── generate_itinerary.py
│   ├── recommend_activities.py
│   ├── fetch_useful_links.py
│   ├── weather_forecaster.py
│   ├── packing_list_generator.py
│   ├── food_culture_recommender.py
│   └── chat_agent.py
│
├── export_utils.py
├── travel_agent.py
├── requirements.txt
└── .env
```

- **agents/**: Contains individual Python scripts for each agent, modularizing the logic.
- **export_utils.py**: Houses shared utility functions (e.g., PDF export).
- **travel_agent.py**: The main Streamlit application file that orchestrates the workflow and UI.
- **requirements.txt**: Lists project dependencies.
- **.env**: Stores environment variables (e.g., `SERPER_API_KEY`).

## Setup Instructions

### Prerequisites
- Python 3.8 or higher.
- OPENAI API key.
- A Google Serper API key.

### Installation
1. Install dependencies:
   ```bash
   uv sync
   ```

2. Set up environment variables:
   - Create a `.env` file in the root directory:
     ```bash
     SERPER_API_KEY=your_api_key_here
     OPENAI_GPT4_API_KEY=your_api_key_here
     HOST_JPE=your_base_url  # Optional, for custom OpenAI endpoints
     ```

3. **🆕 Initialize ChromaDB with Vietnamese travel data:**
   ```bash
   uv run python setup_chromadb.py
   ```
   This will create and populate the vector database with local Vietnamese travel knowledge.

### Running the Application
1. Launch the Streamlit app:
   ```bash
   streamlit run travel_agent.py
   ```

## Usage
- Enter your travel preferences (destination, month, duration, etc.) in the form.
- Click "Generate Itinerary" to create a base plan.
- Use the buttons to fetch additional details (e.g., activity suggestions, weather forecast).
- Interact with the chat to ask questions about your itinerary.
- Export the itinerary as a PDF using the "Export as PDF" button.

## Contributing
Feel free to fork this repository, submit issues, or create pull requests to enhance the project. Contributions to improve agent logic, UI, or add new features are welcome!

## License
This project is open-source. See the [LICENSE](LICENSE) file for details (if applicable).

## Acknowledgements
- Built with Streamlit, LangGraph, LangChain, and Ollama.
- Thanks to the open-source community for tools and libraries!

## Contact
For questions or support, reach out to me on LinkedIn: [Vikram Bhat](https://www.linkedin.com/in/vikrambhat249/) or open an issue in the repository.
