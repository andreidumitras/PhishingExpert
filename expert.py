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

    # def prepare(self, prompt: str) -> None:
    #     response= self.client.chat.completions.create(
    #         model = self.model,
    #         messages = [
    #             {
    #                 "role": "system",
    #                 "content": "You are a helpful assistant that answers only with yes or no."
    #             },
    #             {
    #                 "role": "user",
    #                 "content": prompt
    #             }
    #         ],
    #         max_tokens=5,
    #         temperature=0.1
    #     )
    
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
                    "content": "memorise the following input because you'll receive some questions about it."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=5,
            temperature=0.1
        )
        
    # interacting with the LLM
    def ask(self, prompt: str) -> float:
        # creating a response
        response = self.client.chat.completions.create(
            model = self.model,
            messages = [
                {
                    "role": "system",
                    "content": "Remember the previously input and answer only with one of the following answers: 'very sure', 'sure', 'uncertain', 'clueless'."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=10,
            temperature=0.1
        )
        answer = response.choices[0].message.content.lower()
        # percentage_pattern = r"[\d\.]+%"
        # matches = regex.search(percentage_pattern, answer)
        # if not matches:
        #     return 0
        # percentage = float(matches.group(0).strip('%'))
        
        if "very sure" in answer:
            return 1
        elif "sure" in answer:
            return 0.7
        elif "uncertain" in answer:
            return 0.4
        elif "clueless" in answer:
            return 0
        return 0
        # returns the numeric value of the percentage, without any other characters        
        # return percentage / 100

def ask_about(content, llm, questions: list, typeoftext:str) -> list:
    analysis = []
    if not content or content == "":
        for _ in range(len(questions)):
            analysis.append(0)
        return analysis
    
    llm.analyse(f"Please memorise the following {typeoftext}:\n" + content)
    for q in questions:
        analysis.append(llm.ask(q))
    return analysis
