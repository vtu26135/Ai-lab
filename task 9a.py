# Install the OpenAI library (if not installed)
# pip install openai

from openai import OpenAI
import os

# Load your API key from an environment variable for security
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Give me 3 project ideas I could build using OpenAI APIs."}
    ]
)

print(response.choices[0].message.content)
