import os
import yaml
from dotenv import load_dotenv
from pyprojroot import here

load_dotenv()


class LoadToolsConfig:

    def __init__(self) -> None:
        with open(here("configs/tools_config.yml")) as cfg:
            app_config = yaml.load(cfg, Loader=yaml.FullLoader)

        # Set environment variables
        os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
        os.environ['TAVILY_API_KEY'] = os.getenv("TAVILY_API_KEY")
        os.environ['EMBEDDINGS_API_KEY'] = os.getenv("EMBEDDINGS_API_KEY")
        os.environ['HOST_USE'] = os.getenv("HOST_USE")
        
        # Primary agent
        self.primary_agent_llm = app_config["primary_agent"]["llm"]
        self.primary_agent_llm_temperature = app_config["primary_agent"]["llm_temperature"]

        # Internet Search config
        self.tavily_search_max_results = int(
            app_config["tavily_search_api"]["tavily_search_max_results"])
        
        # Stories RAG configs
        self.stories_rag_llm = app_config["stories_rag"]["llm"]
        self.stories_rag_llm_temperature = float(
            app_config["stories_rag"]["llm_temperature"])
        self.stories_rag_embedding_model = app_config["stories_rag"]["embedding_model"]
        self.stories_rag_vectordb_directory = str(here(
            app_config["stories_rag"]["vectordb"]))
        self.stories_rag_unstructured_docs_directory = str(here(
            app_config["stories_rag"]["unstructured_docs"]))
        self.stories_rag_k = app_config["stories_rag"]["k"]
        self.stories_rag_chunk_size = app_config["stories_rag"]["chunk_size"]
        self.stories_rag_chunk_overlap = app_config["stories_rag"]["chunk_overlap"]
        self.stories_rag_collection_name = app_config["stories_rag"]["collection_name"]

        # Vietnam Travel RAG configs
        self.vietnam_travel_rag_llm = app_config["vietnam_travel_rag"]["llm"]
        self.vietnam_travel_rag_llm_temperature = float(
            app_config["vietnam_travel_rag"]["llm_temperature"])
        self.vietnam_travel_rag_embedding_model = app_config["vietnam_travel_rag"]["embedding_model"]
        self.vietnam_travel_rag_vectordb_directory = str(here(
            app_config["vietnam_travel_rag"]["vectordb"]))
        self.vietnam_travel_rag_unstructured_docs_directory = str(here(
            app_config["vietnam_travel_rag"]["unstructured_docs"]))
        self.vietnam_travel_rag_k = app_config["vietnam_travel_rag"]["k"]
        self.vietnam_travel_rag_chunk_size = app_config["vietnam_travel_rag"]["chunk_size"]
        self.vietnam_travel_rag_chunk_overlap = app_config["vietnam_travel_rag"]["chunk_overlap"]
        self.vietnam_travel_rag_collection_name = app_config["vietnam_travel_rag"]["collection_name"]

        # Graph configs
        self.thread_id = str(
            app_config["graph_configs"]["thread_id"])
