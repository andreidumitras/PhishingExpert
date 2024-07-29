from openai import OpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
import regex

class Expert:
    def __init__(self, model: str | None):
        self.model = model
        # Point to the local serverclient
        self.client = OpenAI(base_url = "http://localhost:1234/v1", api_key = "lm-studio")
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
        self.client.chat.completions.create(
            model = self.model,
            messages = [
                {
                    "role": "system",
                    "content": "You are helpful assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
    
    def analyse(self, prompt: str) -> None:
        # trimming in chunks i case of too large prompt
        if len(prompt) > self.MAX_CHARACTERS_CHUNK_SIZE:
            prompt = self.get_first_chunk(prompt)
        # creating a response
        self.client.chat.completions.create(
            model = self.model,
            messages = [
                {
                    "role": "system",
                    "content": "You are helpful assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
    # interacting with the LLM
    def ask(self, prompt: str) -> float:
        # creating a response
        response = self.client.chat.completions.create(
            model = self.model,
            messages = [
                {
                    "role": "system",
                    "content": "You are helpful assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        answer = response.choices[0].message.content
        percentage_pattern = r"[\d\.]+%"
        matches = regex.search(percentage_pattern, answer)
        if not matches:
            return 0
        percentage = float(matches.group(0).strip('%'))
        # returns the numeric value of the percentage, without any other characters        
        return percentage / 100

def ask_about(content, llm, questions: list, typeoftext:str) -> list:
    analysis = []
    if not content or content == "":
        for _ in range(len(questions)):
            analysis.append(0)
        return analysis
    llm.prepare(f"In this session, I will provide you with an {typeoftext}. After sharing the text, I will ask you a series of questions related to it in subsequent prompts. Please read and understand the text thoroughly, as your future responses will be based on it. When answering my questions, please provide your response in the following format: 'percentage%: short explanation under 50 words'. For example: '80%: The tone of the text has high chances to have an urgent tone.'. First, pease conform with 'yes' if you are ready to receive.")
    llm.analyse("This is the text, confirm with 'Ok' when you receive it:\n" + content.full)
    for q in questions:
        analysis.append(llm.ask(q))
    return analysis
