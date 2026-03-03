from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


client = OpenAI()

def general_chain(query):
    response = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {
                "role": "system",
                "content": "You are a friendly assistant for a retail store. "
                           "Keep responses short and casual. "
                           "If asked anything about products or policies, "
                           "let the user know you can help with that separately."
            },
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content

if __name__=="__main__":
    print(general_chain("Hi"))