import requests
import os
from dotenv import load_dotenv

# .env file se API keys load karein
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Function: Groq AI se response lena
def get_groq_response(prompt):
    url =  "https://api.groq.com/openai/v1/chat/completions"  
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",  # Model ka naam, API docs se check karein
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.text}"

# Function: Tavily API se web search karna
def web_search(query):
    url = f"https://api.tavily.com/v1/search?api_key={TAVILY_API_KEY}&query={query}&num_results=3"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return [result["url"] for result in data["results"]]
    else:
        return f"Error: {response.text}"

# Test Run
if __name__ == "__main__":
    user_input = input("Aapka sawaal: ")
    ai_response = get_groq_response(user_input)
    print("\n🤖 AI Response:", ai_response)

    search_results = web_search(user_input)
    print("\n🌐 Related Searches:", search_results)
