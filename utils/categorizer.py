import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://finsight.streamlit.app",
    "X-Title": "FinSight AI Categorizer"
}

ALLOWED_CATEGORIES = ['Food', 'Travel', 'Shopping', 'Bills', 'Entertainment', 'Other']

def get_free_model():
    try:
        resp = requests.get("https://openrouter.ai/api/v1/models", headers={"Authorization": f"Bearer {API_KEY}"})
        data = resp.json()

        if "data" not in data:
            raise Exception("No model data returned.")

        for model in data["data"]:
            if ":free" in model["id"]:
                return model["id"]

        raise Exception("No free models found 😩")
    except Exception as e:
        print(f"[❌] Error getting model: {e}")
        raise

def send_prompt(messages, model):
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.3,
        "stream": False
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        if response.status_code != 200:
            print(f"HTTP error: {response.status_code} → {response.text}")
            raise Exception("Model failed.")
        
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as err:
        print(f"❌ send_prompt failed: {err}")
        raise

def categorize_bulk(transactions):
    try:
        model = get_free_model()
        print(f"[✔] Using free model: {model}")
    except Exception as e:
        print(f"❌ Could not find a free model: {e}")
        return transactions

    sample_txns = transactions[:10]  # Only first 10

    prompt = "Classify each transaction below into one of these categories:\n"
    prompt += f"{ALLOWED_CATEGORIES}\n\nTransactions:\n"
    prompt += "\n".join([f"{i+1}. {t['description']}" for i, t in enumerate(sample_txns)])
    prompt += "\n\nRespond ONLY with a JSON array of categories like:\n[\"Food\", \"Travel\", ...]"

    try:
        reply = send_prompt([{"role": "user", "content": prompt}], model=model)
        print("🤖 Reply from model:", reply)
        categories = json.loads(reply)

        for i in range(len(sample_txns)):
            sample_txns[i]["category"] = (
                categories[i] if categories[i] in ALLOWED_CATEGORIES else "Other"
            )

        return sample_txns
    except Exception as e:
        print(f"Error in bulk categorization: {e}")
        for txn in sample_txns:
            txn["category"] = "Other"
        return sample_txns
