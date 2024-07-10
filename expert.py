from openai import OpenAI
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter

class Expert:
    def __init__(self):
        self.model: str = None
        # Point to the local serverclient
        self.client = OpenAI(base_url = "http://localhost:1234/v1", api_key = "lm-studio")
        self.CHARACTERS_CHUNK_SIZE = 7000
    
    # in case that the prompted text is too large for the LLM.
    # 1 token = 4 characters
    # max tokens = ~2000 => the chunk of characters si around 8000.
    # I chose to split the fayload in chunks of 7000 characters, to let the LLM handle the input
    # first chunk is arguably enough to make an idea of how suspicious an email is.
    def get_first_chunk(self, prompt: str) -> str:
        rec_text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = self.CHARACTERS_CHUNK_SIZE,
            chunk_overlap = 0,
            length_function = len,
        )
        chunks = rec_text_splitter.split_text(prompt)
        return chunks[0]

    # interacting with the LLM
    def ask(self, prompt: str, quiet: bool = False) -> float:
        # trimming in chunks i case of too large prompt
        if len(prompt) > self.CHARACTERS_CHUNK_SIZE:
            prompt = self.get_first_chunk(prompt)
        # creating a response
        response = self.client.chat.completions.create(
            model = self.model,
            messages = [
                {
                    "role": "system",
                    "content": "You are specialist in phishing detection that always provide a probability value that quantifies how the provided aspect exists in the memorized contex. Please always output only the probability percentage, without any explanation"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        # is quiet mode is selected, no result will be returned
        if quiet:
            return None
        answer = response.choices[0].message.content.strip()
        # extract only the percentages from the provided answers
        pattern = re.compile(r"[\d]{1,3}%")
        result = pattern.search(answer)
        # returns the numeric value of the percentage, without any other characters        
        return float(result.group(0).strip('%'))
