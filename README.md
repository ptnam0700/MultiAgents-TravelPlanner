# Vietnam Travel Planner

Welcome to the **Vietnam Travel Planner**, a sophisticated multi-agent system built with Streamlit, LangGraph, and advanced AI technologies. This application leverages multiple specialized AI agents to generate personalized Vietnam travel itineraries with authentic local insights and comprehensive travel information.

## Overview

The Vietnam Travel Planner uses a LangGraph workflow orchestrating multiple intelligent agents that process user preferences to deliver detailed itineraries, activity suggestions, weather forecasts, packing lists, food/culture recommendations, hotel suggestions, and an interactive chat interface.

**🌟 Key Features:**
- **RAG-Enhanced Recommendations**: ChromaDB vector database populated with hidden Vietnamese travel gems, local knowledge, and authentic information from travel blogs and articles
- **Intelligent Search**: Conditional Tavily search integration that supplements local knowledge when needed
- **Multi-Agent Architecture**: Specialized agents working collaboratively through LangGraph workflows
- **Real-time Weather Integration**: Current weather forecasting for travel destinations
- **Interactive Chat**: RAG-powered chat system for answering itinerary-related questions

The system integrates with OpenAI API (GPT-4o-mini model) and Google Serper API for web searches, enhanced with local Vietnamese travel knowledge through semantic search and retrieval-augmented generation.

## Features
- **Smart Itinerary Generation**: Create detailed travel itineraries with daily plans, dining options, and activities
- **Local Activity Recommendations**: Discover unique activities based on your preferences and itinerary
- **Hotel Search**: Find suitable accommodations matching your budget and preferences
- **Weather Forecasting**: Get accurate weather predictions for your travel dates
- **Smart Packing Lists**: Generate customized packing recommendations based on destination and weather
- **Food & Culture Insights**: Authentic Vietnamese cuisine and cultural recommendations
- **Useful Links**: Curated travel guide links and resources
- **RAG-Powered Chat**: Interactive chat system with access to local Vietnamese travel knowledge
- **PDF Export**: Download your complete itinerary as a formatted PDF

## Directory Structure

```
Vietnam-Travel-Planner/
│
├── agents/                          # Individual AI agents
│   ├── generate_itinerary.py       # Main itinerary generation agent
│   ├── recommend_activities.py     # Activity recommendations
│   ├── fetch_useful_links.py       # Travel guide links fetcher
│   ├── weather_forecaster.py       # Weather prediction agent
│   ├── packing_list_generator.py   # Smart packing list generator
│   ├── food_culture_recommender.py # Food & culture insights
│   ├── hotel_search.py             # Hotel recommendations
│   ├── rag_chat_agent.py           # RAG-powered chat interface
│   ├── vietnam_travel_context.py   # Local knowledge retrieval
│   └── conditional_tavily_search.py # Intelligent web search
│
├── src/                            # Core application modules
│   ├── create_vector_db.py         # Vector database setup
│   ├── agent_graph/                # LangGraph workflow definitions
│   ├── chatbot/                    # Chat interface components  
│   ├── config/                     # Configuration management
│   ├── database/                   # Database utilities
│   └── utils/                      # Shared utility functions
│
├── data/                           # Data storage
│   ├── stories_vectordb/           # ChromaDB vector database
│   └── unstructured_docs/          # Source documents for RAG
│
├── configs/                        # Configuration files
├── tests/                          # Test suites
├── travel_agent.py                 # Main Streamlit application
├── utils_export.py                 # PDF export utilities
├── pyproject.toml                  # Project configuration and dependencies
├── requirements.txt                # Legacy dependency list
└── .env                           # Environment variables
```

## Setup Instructions

### Prerequisites
- Python 3.11 (required for compatibility)
- OpenAI API key for GPT-4o-mini model and embeddings
- Google Serper API key for web search functionality
- Tavily API key for conditional web search
- (Optional) LangSmith API key for development tracing
- (Optional) Custom OpenAI-compatible API endpoints

### Installation

1. **Clone and navigate to the project:**
   ```bash
   git clone <repository-url>
   cd Vietnam-Travel-Planner
   ```

2. **Install dependencies using uv:**
   ```bash
   uv sync
   ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```bash
   # Required API keys
   OPENAI_API_KEY=your_openai_api_key_here
   SERPER_API_KEY=your_serper_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   EMBEDDINGS_API_KEY=your_embeddings_api_key_here
   
   # Optional: LangSmith for tracing (recommended for development)
   LANGSMITH_API_KEY=your_langsmith_api_key_here
   
   # Custom API endpoints (if using custom OpenAI-compatible services)
   HOST_JPE=your_custom_openai_base_url
   HOST_USE=your_custom_embeddings_base_url
   
   # Embedding model configuration
   EMBEDDINGS_MODEL=text-embedding-3-small
   ```

4. **Initialize the ChromaDB vector database:**
   ```bash
   uv run python src/create_vector_db.py
   ```
   This creates and populates the vector database with Vietnamese travel knowledge from documents in `data/unstructured_docs/`.

### Running the Application

1. **Launch the Streamlit application:**
   ```bash
   uv run streamlit run travel_agent.py
   ```

2. **Access the application:**
   Open your browser and navigate to the provided local URL (typically `http://localhost:8501`)

## Usage

### Planning Your Trip
1. **Fill out the travel form** with your preferences:
   - Destination in Vietnam
   - Number of travelers
   - Travel dates
   - Holiday type (Party, Adventure, Family, etc.)
   - Budget level (Budget, Mid-Range, Luxury, etc.)
   - Additional comments or specific requirements

2. **Generate your base itinerary** by clicking "Generate Itinerary"
   - The system uses RAG to access local Vietnamese knowledge
   - Performs conditional web searches when needed
   - Integrates real-time weather data
   - Creates a detailed day-by-day plan

### Enhancing Your Experience
3. **Use the specialized agent buttons** to get additional insights:
   - **🎯 Activity Suggestions**: Discover unique local activities
   - **🔗 Useful Links**: Get curated travel guide resources
   - **🌤️ Weather Forecast**: View detailed weather predictions
   - **🎒 Packing List**: Generate smart packing recommendations
   - **🍽️ Food & Culture**: Explore authentic Vietnamese cuisine and culture
   - **🏨 Hotels**: Find accommodation recommendations

4. **Chat with the RAG system** to ask specific questions about:
   - Your itinerary details
   - Local customs and etiquette
   - Hidden gems and off-the-beaten-path locations
   - Transportation options
   - Cultural insights

5. **Export your complete itinerary** as a PDF for offline access

## Technical Architecture

### Core Technologies
- **Frontend**: Streamlit for interactive web interface
- **Workflow Orchestration**: LangGraph for managing multi-agent workflows
- **Language Models**: OpenAI GPT-4o-mini for natural language processing
- **Vector Database**: ChromaDB for semantic search and RAG functionality
- **Embeddings**: OpenAI embeddings for document vectorization
- **Web Search**: Google Serper API and conditional Tavily search integration

### Agent Workflow
The system follows a structured workflow:
1. **Vietnam Context Lookup**: Retrieves relevant local knowledge from the vector database
2. **Conditional Tavily Search**: Supplements knowledge with web search when needed
3. **Weather Integration**: Fetches current weather data for destinations
4. **Itinerary Generation**: Creates comprehensive travel plans using all gathered information

### RAG System
The Retrieval-Augmented Generation system enhances recommendations with:
- Local Vietnamese travel knowledge from curated documents
- Hidden gems and off-the-beaten-path locations
- Cultural insights and etiquette guidelines
- Authentic food and activity recommendations

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Areas for Contribution
- Additional travel agents (e.g., transportation, visa information)
- Enhanced UI/UX improvements
- Integration with more travel APIs
- Support for other Southeast Asian countries
- Performance optimizations
- Test coverage improvements

## License

This project is open-source. Please check the repository for license details.

## Acknowledgements

- **LangChain & LangGraph**: For powerful AI agent orchestration capabilities
- **Streamlit**: For rapid web application development
- **ChromaDB**: For efficient vector database operations
- **OpenAI**: For advanced language models and embeddings
- **Vietnamese Travel Community**: For providing authentic local knowledge and insights

## Support

For questions, issues, or support:
- Open an issue in the GitHub repository
- Check existing issues and discussions
- Contribute to the project documentation
