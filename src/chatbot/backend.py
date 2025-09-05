from typing import List

from agent_graph.build_full_graph import build_graph
from agent_graph.load_tools_config import LoadToolsConfig
from agent_graph.tool_stories_rag import StoriesRAGTool
from chatbot.load_config import LoadProjectConfig


PROJECT_CFG = LoadProjectConfig()
TOOLS_CFG = LoadToolsConfig()

graph = build_graph()
config = {"configurable": {"thread_id": TOOLS_CFG.thread_id}}

# create_directory("memory")


class ChatBot:
    """
    A class to handle chatbot interactions by utilizing a pre-defined agent graph. The chatbot processes
    user messages, generates appropriate responses, and saves the chat history to a specified memory directory.

    Attributes:
        config (dict): A configuration dictionary that stores specific settings such as the `thread_id`.

    Methods:
        respond(chatbot: List, message: str) -> str:
            Processes the user message through the agent graph, generates a response, and saves the chat history.
    """
    @staticmethod
    def respond(chatbot: List, message: str) -> str:
        """
        Processes a user message using the agent graph, generates a response, and saves the chat history.

        Args:
            chatbot (List): A list representing the chatbot conversation history. Each entry is a dict with role and content.
            message (str): The user message to process.

        Returns:
            str: The assistant's response message.
        """
        # The config is the **second positional argument** to stream() or invoke()!
        events = graph.stream(
            {"messages": [("user", message)]}, config, stream_mode="values"
        )
        
        response_content = ""
        for event in events:
            response_content = event["messages"][-1].content
            event["messages"][-1].pretty_print()
            
        # Update conversation with the new assistant message
        chatbot.append({"role": "assistant", "content": response_content})

        # Memory.write_chat_history_to_file(
        #     gradio_chatbot=chatbot, folder_path=PROJECT_CFG.memory_dir, thread_id=TOOLS_CFG.thread_id)
        
        return response_content
