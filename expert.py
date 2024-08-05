from openai import OpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
import regex

class Expert:
    def __init__(self, model: str):
        # self.API_KEY = "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"
        self.model = model
        # Point to the local serverclient
        self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
        self.MAX_CHARACTERS_CHUNK_SIZE = 7000
    
    def get_first_chunk(self, prompt: str) -> str:
        # in case that the prompted text is too large for the LLM.
        # 1 token = 4 characters
        # max tokens = ~2000 => the chunk of characters si around 8000.
        # I chose to split the fayload in chunks of 7000 characters, to let the LLM handle the input
        # first chunk is arguably enough to make an idea of how suspicious an email is.
        rec_text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = self.MAX_CHARACTERS_CHUNK_SIZE,
            chunk_overlap = 0,
            length_function = len,
        )
        chunks = rec_text_splitter.split_text(prompt)
        return chunks[0]

    def prepare(self, prompt: str) -> None:
        response= self.client.chat.completions.create(
            model = self.model,
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that answers only with yes or no."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=5,
            temperature=0.1
        )
        print(response.choices[0].message.content)
    
    def analyse(self, prompt: str) -> None:
        # trimming in chunks i case of too large prompt
        if len(prompt) > self.MAX_CHARACTERS_CHUNK_SIZE:
            prompt = self.get_first_chunk(prompt)
        # creating a response
        response = self.client.chat.completions.create(
            model = self.model,
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that answers only with OK or not Ok"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=5,
            temperature=0.1
        )
        print(response)
        
    # interacting with the LLM
    def ask(self, prompt: str) -> float:
        # creating a response
        response = self.client.chat.completions.create(
            model = self.model,
            messages = [
                {
                    "role": "system",
                    "content": "You are helpful assistant that will answer only using percentages that corresponds to which extent the future question is valid to the previously given text."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=120,
            temperature=0.1
        )
        answer = response.choices[0].message.content
        percentage_pattern = r"[\d\.]+%"
        matches = regex.search(percentage_pattern, answer)
        if not matches:
            return 0
        percentage = float(matches.group(0).strip('%'))
        print(answer)
        print(f"percentage: {percentage}")
        # returns the numeric value of the percentage, without any other characters        
        return percentage / 100

def ask_about(content, llm, questions: list, typeoftext:str) -> list:
    analysis = []
    if not content or content == "":
        for _ in range(len(questions)):
            analysis.append(0)
        return analysis
    
    llm.prepare(f"In this session, I will provide you with an {typeoftext}. After sharing the text, I will ask you memorize the text because I will give you a series of questions related to it in subsequent prompts. Please read and understand the text thoroughly, as your future responses will be based on it. When answering my questions, please provide only the percentage amount of how valid is the question for the provided text.")
    llm.analyse("This is the text to memorize:\n" + content)
    for q in questions:
        analysis.append(llm.ask(q))
    return analysis
