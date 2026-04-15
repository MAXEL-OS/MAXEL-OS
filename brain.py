import requests

MODEL_NAME = "maxel-brain"

def call_ollama(prompt, history):
    # Format previous messages for context
    context = ""
    for msg in history:
        role_label = "User" if msg["role"] == "user" else "AI"
        context += f"{role_label}: {msg['content']}\n"
    
    # Mirror language logic
    is_arabic = any('\u0600' <= c <= '\u06FF' for c in prompt)
    system_instruction = "IMPORTANT: Reply ONLY in Arabic." if is_arabic else "IMPORTANT: Reply ONLY in English."
    
    payload = {
        "model": MODEL_NAME,
        "prompt": f"{context}System: {system_instruction}\nUser: {prompt}\nAI:",
        "stream": False
    }
    
    try:
        r = requests.post("http://localhost:11434/api/generate", json=payload, timeout=600)
        response = r.json().get("response", "Error: Empty response")
        return response
    except Exception as e:
        return f"System Core Error: {str(e)}"
