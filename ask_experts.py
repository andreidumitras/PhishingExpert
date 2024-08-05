from groq import Groq
import sys

client = Groq(api_key="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")

def ask(prompt: str):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gemma2-9b-it",
        # model="llama3-70b-8192",
    )
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    for i in range(25):
        print(f"Request{i}:")
        print(ask(f"What's {i} squareed?"))
    