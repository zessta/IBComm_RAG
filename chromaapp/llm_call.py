# Model Call
import requests
from dotenv import load_dotenv
import os

load_dotenv()
llm_token = os.getenv("token")


def chat_with_model(text, query):
    print(text)
    url = "http://74.225.221.182:8000/v1/chat/completions"
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
        f"This is the source text:\n{source_text}\n\n"
        f"Using only the information in the source, answer the following question as accurately and precisely as possible. "
        f"The answer should be directly based on the content of the source, must include only the most important and relevant details, "
        f"and use your intuition like a human.\n\n"
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
