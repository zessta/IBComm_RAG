# Model Call
import requests
from dotenv import load_dotenv
import os

load_dotenv()
llm_token = os.getenv("token")


def chat_with_model(text, query):
    
    # url = "http://74.225.221.182:8000/v1/chat/completions"
    url = "http://127.0.0.1:8000/v1/chat/completions"
    token = llm_token
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Join list of strings if necessary
    if isinstance(text, list):
        source_text = "\n\n".join(text)
    else:
        source_text = text

    prompt = (
    f"This is the source text (a group conversation log):\n{source_text}\n\n"
    f"Based solely on the information in the source, answer the following question as accurately and precisely as possible. "
    f"The answer must be grounded in the content, follow the sequence of events described, and include only the most relevant and important actions. "
    f"Use human-like reasoning to organize the response clearly and chronologically.\n\n"
    f"Question: {query}"
)



    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"Error {response.status_code}: {response.text}"
