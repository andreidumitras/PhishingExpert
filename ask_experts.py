from openai import OpenAI
from langdetect import detect

# Point to the local server
client = OpenAI(base_url = "http://localhost:1234/v1", api_key = "lm-studio")

def chat_with_expert(prompt):
    response = client.chat.completions.create(
        model = "lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
        # NOTE:
        #   system:     it modifies the personality of the model
        #   user:       the user query
        #   assistant:  give examples of desired behaviours
        # messages variable gives a short experience for the model in order to answer properly.
        messages = [
            {
                "role": "system",
                "content": "You are an expert in detecting manipulative language and phishing attacks. You provide answers in percentage, follow by a short explanation."
            },
            {
                "role": "user",
                "content": prompt
            },
            {
                "role": "assistant",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content.strip()

#   temperature=0.7,

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break
        response = chat_with_expert(user_input)
        print("Chatbot: ", response)
