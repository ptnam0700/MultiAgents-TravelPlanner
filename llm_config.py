from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class LLMConfig:
    """Centralized LLM configuration and factory for the travel planner application."""
    
    @staticmethod
    def get_openai_llm(model: str = "gpt-4o-mini", temperature: float = 0.7) -> ChatOpenAI:
        """
        Get configured OpenAI ChatGPT model.
        
        Args:
            model: Model name (default: gpt-4o-mini)
            temperature: Sampling temperature (default: 0.7)
            
        Returns:
            Configured ChatOpenAI instance
        """
        return ChatOpenAI(
            model=model,
            api_key=os.getenv("OPENAI_GPT4_API_KEY"),
            base_url=os.getenv("HOST_JPE"),
            temperature=temperature
        )

    @staticmethod
    def validate_config() -> dict:
        """
        Validate that required environment variables are set.
        
        Returns:
            Dictionary with validation results
        """
        validation_results = {
            "openai_configured": bool(os.getenv("OPENAI_GPT4_API_KEY")),
            "azure_configured": all([
                os.getenv("AZURE_OPENAI_API_KEY"),
                os.getenv("AZURE_OPENAI_ENDPOINT"),
                os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
            ]),
            "missing_vars": []
        }
        
        # Check OpenAI vars
        if not os.getenv("OPENAI_GPT4_API_KEY"):
            validation_results["missing_vars"].append("OPENAI_GPT4_API_KEY")
        
        # Check Azure vars
        azure_vars = ["AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_DEPLOYMENT_NAME"]
        for var in azure_vars:
            if not os.getenv(var):
                validation_results["missing_vars"].append(var)
        
        return validation_results