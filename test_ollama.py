import ollama

print("Connecting to Ollama...")

response = ollama.chat(
    model="llama3.2:latest",
    messages=[
        {
            "role": "user",
            "content": "Give me one simple viva question about an AI Autonomous Research Workplace."
        }
    ]
)

print("AI Response:")
print(response["message"]["content"])