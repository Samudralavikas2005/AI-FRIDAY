# ai/gemini_client.py
import requests
import re
from config import GEMINI_API_KEY, GEMINI_ENDPOINT

class GeminiClient:
    def __init__(self):
        pass
    
    def query_gemini(self, prompt, conversation_history):
        if not GEMINI_API_KEY:
            return "Gemini API key not set. Please configure GEMINI_API_KEY."
        try:
            conversation_history_flat = []
            for day_entries in conversation_history.values():
                for turn in day_entries:
                    conversation_history_flat.append({"role": "user", "text": turn["q"]})
                    conversation_history_flat.append({"role": "assistant", "text": turn["a"]})
            conversation_history_flat.append({"role": "user", "text": prompt})

            contents = []
            for turn in conversation_history_flat[-20:]:
                if turn["role"] == "user":
                    contents.append({"role": "user", "parts": [{"text": turn["text"]}]})
                else:
                    contents.append({"role": "model", "parts": [{"text": turn["text"]}]})

            headers = {"Content-Type": "application/json"}
            payload = {"contents": contents, "generationConfig": {"maxOutputTokens": 200}}
            url = f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}"

            response = requests.post(url, json=payload, headers=headers, timeout=30)
            data = response.json()

            candidates = data.get("candidates", [])
            if candidates and "content" in candidates[0]:
                parts = candidates[0]["content"].get("parts", [])
                if parts and "text" in parts[0]:
                    gemini_text = parts[0]["text"]
                    cleaned_text = self.clean_markdown(gemini_text)
                    print("\n🤖 Friday says (contextual):\n", cleaned_text, "\n")
                    return cleaned_text
            return "Gemini did not return a valid response."
        except Exception as e:
            return f"Gemini API error: {e}"

    def clean_markdown(self, text):
        text = re.sub(r'(\*\*|__|\*|_)', '', text)
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*[\*\-]\s+', '', text, flags=re.MULTILINE)
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\s{2,}', ' ', text)
        return text.strip()
