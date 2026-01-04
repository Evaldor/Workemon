import requests
import logging
import os

logger = logging.getLogger(__name__)

class LLMHandler:
    def __init__(self):
        self.provider = os.getenv('LLM_PROVIDER', 'yandex')
        self.api_keys = {
            'yandex': os.getenv('YANDEX_GPT_API_KEY'),
            'deepseek': os.getenv('DEEPSEEK_API_KEY'),
            'grok': os.getenv('GROK_API_KEY'),
        }
        if not self.api_keys.get(self.provider):
            raise ValueError(f"API key for {self.provider} not set")

    def call_llm(self, prompt):
        """Call the configured LLM with the prompt."""
        try:
            if self.provider == 'yandex':
                return self._call_yandex(prompt)
            elif self.provider == 'deepseek':
                return self._call_deepseek(prompt)
            elif self.provider == 'grok':
                return self._call_grok(prompt)
            else:
                raise ValueError("Unknown LLM provider")
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return "Error: Failed to get response from LLM"

    def _call_yandex(self, prompt):
        # Placeholder for Yandex GPT API
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {"Authorization": f"Api-Key {self.api_keys['yandex']}"}
        data = {
            "modelUri": "gpt://your-folder-id/yandexgpt-lite",  # Adjust as needed
            "completionOptions": {"stream": False, "temperature": 0.6, "maxTokens": 2000},
            "messages": [{"role": "user", "text": prompt}]
        }
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result['result']['alternatives'][0]['message']['text']

    def _call_deepseek(self, prompt):
        # Placeholder for DeepSeek API
        url = "https://api.deepseek.com/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_keys['deepseek']}"}
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']

    def _call_grok(self, prompt):
        # Placeholder for Grok API
        url = "https://api.x.ai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_keys['grok']}"}
        data = {
            "model": "grok-1",
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']