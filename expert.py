from openai import OpenAI
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter

class Expert:
    def __init__(self):
        self.model: str = None
        # Point to the local serverclient = 
        self.client = OpenAI(base_url = "http://localhost:1234/v1", api_key = "lm-studio")
        # self.numeric_answer: float = None
        # self.explanation: str = None
        self.CHARACTERS_CHUNK_SIZE = 7000
        
    def get_first_chunk(self, prompt: str) -> str:
        rec_text_splitter = RecursiveCharacterTextSplitter(
            chunks_size = self.CHARACTERS_CHUNK_SIZE,
            chunk_overlap = 0,
            length_function = len,
        )
        chunks = rec_text_splitter.split_text(prompt)
        return chunks[0]


    def ask(self, prompt: str, quiet: bool = False) -> float:
        if len(prompt) > self.CHARACTERS_CHUNK_SIZE:
            prompt = self.get_first_chunk(prompt)
        response = self.client.chat.completions.create(
            model = self.model,
            messages = [
                {
                    "role": "system",
                    "content": "You are specialist in phishing detection that always provide a probability value that quantifies how the provided aspect exists in the memorized contex. You will always put the percentage as the first word as shown here: 87% your explanation."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        if quiet:
            return None
        answer = response.choices[0].message.content.strip()
        # index = answer[0].rfind(' ')
        # self.numeric_answer = float(int(answer[0][13:]) / 100)
        # self.explanation = answer[1].strip()
        # return list([self.numeric_answer, self.explanation])
        # return self.extract_values(answer)
# >>> p = re.compile("name (.*) is valid")
# >>> result = p.search(s)
# >>> result
# <_sre.SRE_Match object at 0x10555e738>
# >>> result.group(1)
        pattern = re.compile(r"[\d]{1,3}%")
        result = pattern.search(answer)
        return float(result.group(0).strip('%'))
        # return answer
