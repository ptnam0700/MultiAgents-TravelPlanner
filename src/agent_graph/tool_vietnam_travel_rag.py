from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.tools import tool
from agent_graph.load_tools_config import LoadToolsConfig
import os
from typing import Optional, List

TOOLS_CFG = LoadToolsConfig()


class VietnamTravelRAGTool:
    """
    A tool for retrieving relevant Vietnam travel information using a Retrieval-Augmented Generation (RAG) approach with vector embeddings.

    This tool leverages a pre-trained OpenAI embedding model to transform user queries into vector embeddings.
    It then uses these embeddings to query a Chroma-based vector database to retrieve the top-k most relevant
    Vietnam travel documents from a specific collection stored in the database.

    The tool supports category-based filtering to search within specific travel categories:
    - hidden_gems: Lesser-known attractions and places
    - food_culture: Local cuisine, restaurants, and food experiences  
    - local_insights: Cultural tips, customs, and local perspectives
    - practical_tips: Transportation, accommodation, and practical advice

    Attributes:
        embedding_model (str): The name of the OpenAI embedding model used for generating vector representations of queries.
        vectordb_dir (str): The directory where the Chroma vector database is persisted on disk.
        k (int): The number of top-k nearest neighbor documents to retrieve from the vector database.
        vectordb (Chroma): The Chroma vector database instance connected to the specified collection and embedding model.

    Methods:
        __init__: Initializes the tool with the specified embedding model, vector database, and retrieval parameters.
        search: Retrieves relevant documents based on query and optional category filter.
    """

    def __init__(self, embedding_model: str, vectordb_dir: str, k: int, collection_name: str) -> None:
        """
        Initializes the VietnamTravelRAGTool with the necessary configurations.

        Args:
            embedding_model (str): The name of the embedding model (e.g., "text-embedding-3-small")
                used to convert queries into vector representations.
            vectordb_dir (str): The directory path where the Chroma vector database is stored and persisted on disk.
            k (int): The number of nearest neighbor documents to retrieve based on query similarity.
            collection_name (str): The name of the collection inside the vector database that holds the relevant travel documents.
        """
        self.embedding_model = embedding_model
        self.vectordb_dir = vectordb_dir
        self.k = k
        self.vectordb = Chroma(
            collection_name=collection_name,
            persist_directory=self.vectordb_dir,
            embedding_function=OpenAIEmbeddings(
                model=self.embedding_model,
                base_url=os.getenv("HOST_USE"),
                api_key=os.getenv("EMBEDDINGS_API_KEY"),
            )
        )
        print("Number of vectors in Vietnam travel vectordb:",
            self.vectordb._collection.count(), "\n\n")

    def search(self, query: str, category: Optional[str] = None) -> List[str]:
        """
        Search for relevant Vietnam travel information.

        Args:
            query (str): The search query
            category (str, optional): Filter by category (hidden_gems, food_culture, local_insights, practical_tips)

        Returns:
            List[str]: List of relevant document contents
        """
        if category:
            # Use metadata filtering if category is specified
            docs = self.vectordb.similarity_search(
                query, 
                k=self.k,
                filter={"category": category}
            )
        else:
            # Search across all categories
            docs = self.vectordb.similarity_search(query, k=self.k)
        
        return [doc.page_content for doc in docs]


@tool
def lookup_vietnam_travel(query: str, category: str = None) -> str:
    """Search Vietnam travel information and find answers to travel-related queries. 
    
    Args:
        query: The travel-related question or search query
        category: Optional category filter - one of: hidden_gems, food_culture, local_insights, practical_tips
        
    Returns:
        Relevant Vietnam travel information based on the query
    """
    rag_tool = VietnamTravelRAGTool(
        embedding_model=TOOLS_CFG.vietnam_travel_rag_embedding_model,
        vectordb_dir=TOOLS_CFG.vietnam_travel_rag_vectordb_directory,
        k=TOOLS_CFG.vietnam_travel_rag_k,
        collection_name=TOOLS_CFG.vietnam_travel_rag_collection_name
    )
    
    docs = rag_tool.search(query, category)
    return "\n\n".join(docs)