
from config import LLM_PROVIDER, MODEL, OLLAMA_HOST


from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

class LLMInterface:
    def __init__(self):
        self.provider = LLM_PROVIDER
        self.model = MODEL
        self.temperature = 0.7

        if self.provider == "openai":
            self.llm = ChatOpenAI(model=self.model, temperature=self.temperature)
        elif self.provider == "ollama":
            self.llm = ChatOllama(model=self.model, temperature=self.temperature, base_url=OLLAMA_HOST)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def generate(self, prompt: str, verbose: bool = False) -> str:
        if verbose:
            print("********************************")
            print("********************************")
            print("********************************")
            print(prompt)
        return self._call_langchain(prompt)

    def _call_langchain(self, prompt: str, verbose: bool = False) -> str:
        response = self.llm.invoke([HumanMessage(content=prompt)])
        if verbose:
            print("-------------------------------------------------")
            print("-------------------------------------------------")
            print("-------------------------------------------------")
            print(response)
        if isinstance(response.content, str):
            return response.content.strip()
        return "".join(str(x) for x in response.content).strip()



