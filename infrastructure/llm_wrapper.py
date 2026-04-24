from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from domain.interfaces import ILLM
from infrastructure.config import GROQ_API_KEY

class LLMWrapper(ILLM):
    def __init__(self):
        self.llm = ChatGroq(model_name="llama-3.1-8b-instant", groq_api_key=GROQ_API_KEY, temperature=0.1)

    def invoke(self, prompt: str) -> str:
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content
        
    def invoke_with_system(self, system_message: str, human_message: str) -> str:
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=human_message)
        ]
        response = self.llm.invoke(messages)
        return response.content
