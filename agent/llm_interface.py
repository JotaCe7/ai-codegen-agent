
# from config import LLM_PROVIDER, MODEL, OLLAMA_HOST


# from langchain_openai import ChatOpenAI
# from langchain_ollama import ChatOllama
# from langchain_core.messages import HumanMessage

# class LLMInterface:
#     def __init__(self):
#         self.provider = LLM_PROVIDER
#         self.model = MODEL
#         self.temperature = 0.7

#         if self.provider == "openai":
#             self.llm = ChatOpenAI(model=self.model, temperature=self.temperature)
#         elif self.provider == "ollama":
#             self.llm = ChatOllama(model=self.model, temperature=self.temperature, base_url=OLLAMA_HOST)
#         else:
#             raise ValueError(f"Unsupported provider: {self.provider}")

#     def generate(self, prompt: str, verbose: bool = False) -> str:
#         if verbose:
#             print("********************************")
#             print("********************************")
#             print("********************************")
#             print(prompt)
#         return self._call_langchain(prompt)

#     def _call_langchain(self, prompt: str, verbose: bool = False) -> str:
#         response = self.llm.invoke([HumanMessage(content=prompt)])
#         if verbose:
#             print("-------------------------------------------------")
#             print("-------------------------------------------------")
#             print("-------------------------------------------------")
#             print(response)
#         if isinstance(response.content, str):
#             return response.content.strip()
#         return "".join(str(x) for x in response.content).strip()



"""
This module provides a standardized interface for interacting with different
language models using the LangChain framework.
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import SecretStr
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

from config import LLM_PROVIDER, MODEL, OPENAI_API_KEY, OLLAMA_HOST

class LLMInterface:
    """A wrapper for language models to provide a consistent interface."""

    def __init__(self):
        """Initializes the LLM interface based on the configured provider."""
        self.provider = LLM_PROVIDER
        self.model_name = MODEL
        self.temperature = 0.7

        if self.provider == "openai":
            self.model = ChatOpenAI(
                model=self.model_name,
                temperature=self.temperature,
                api_key=SecretStr(OPENAI_API_KEY) if OPENAI_API_KEY else None
            )
        elif self.provider == "ollama":
            self.model = ChatOllama(
                model=self.model_name,
                temperature=self.temperature,
                base_url=OLLAMA_HOST
            )
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

        # Define the LangChain processing chain.
        # This combines a prompt template, the model, and an output parser.
        self.prompt_template = ChatPromptTemplate.from_template("{prompt}")
        self.output_parser = StrOutputParser()
        self.chain = self.prompt_template | self.model | self.output_parser

    def generate(self, prompt: str, verbose: bool = False) -> str:
        """Generates a response from the language model using a prompt.

        Args:
            prompt: The input prompt to send to the language model.
            verbose: If True, prints the prompt and raw response.

        Returns:
            A string containing the language model's response.
        """
        if verbose:
            print("\n--- Sending Prompt to LLM ---")
            print(prompt)
            print("-----------------------------")

        # Invoke the LangChain chain with the prompt.
        response = self.chain.invoke({"prompt": prompt})

        if verbose:
            print("\n--- Received LLM Response ---")
            print(response)
            print("-----------------------------")
            
        return response.strip()

