from openai import OpenAI
import os

# Load your API key securely
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = []
system_msg = input("What type of chatbot would you like to create?\n")
messages.append({"role": "system", "content": system_msg})

print("\nYour new assistant is ready! Type your query (type 'quit()' to exit)\n")

while True:
    message = input("You: ")
    if message.lower() == "quit()":
        print("Chat ended.")
        break

    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    print("\nAssistant:", reply, "\n")
