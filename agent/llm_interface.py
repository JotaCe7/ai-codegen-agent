import requests
import openai
from config import LLM_PROVIDER, MODEL, OPENAI_API_KEY, OLLAMA_HOST

class LLMInterface:
    def __init__(self):
        self.provider = LLM_PROVIDER
        self.model = MODEL
        if self.provider == "openai":
            openai.api_key = OPENAI_API_KEY

    def generate(self, prompt: str) -> str:
        if self.provider == "openai":
            return self._call_openai(prompt)
        elif self.provider == "ollama":
            return self._call_ollama(prompt)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def _call_openai(self, prompt: str) -> str:
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    def _call_ollama(self, prompt: str) -> str:
        response = requests.post(
            f"{OLLAMA_HOST}/api/chat",
            json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "stream":False
            }
        )
        if response.status_code != 200:
            raise RuntimeError(f"Ollama call failed: {response.text}")
        return response.json()['message']['content'].strip()
