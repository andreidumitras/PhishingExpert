from openai import OpenAI
import langchain
from langchain.text_splitter import RecursiveCharacterTextSplitter

class Expert:
    def __init__(self):
        self.model: str = None
        # Point to the local serverclient = 
        self.client = OpenAI(base_url = "http://localhost:1234/v1", api_key = "lm-studio")
        self.numeric_answer: float = None
        self.explanation: str = None
        self.CHARACTERS_CHUNK_SIZE = 7000
        
    def get_first_chunk(self, prompt: str) -> str:
        rec_text_splitter = RecursiveCharacterTextSplitter(
            chunc_size = self.CHARACTERS_CHUNK_SIZE,
            chunk_overlap = 0,
            length_function = len,
        )
        chunks = rec_text_splitter.split_text(prompt)
        return chunks[0]

    def topic_message(self, topic: str, prompt: str):
        # NOTE:
            #   system:     it modifies the personality of the model
            #   user:       the user query
            #   assistant:  give examples of desired behaviours
            # messages variable gives a short experience for the model in order to answer properly.
        match topic:
            case 'email_address':        
                messages = [
                    {
                        "role": "system",
                        "content": 'You are specialist in phishing detection that always provide a probability that quantifies how the aspect exists in the provided input.'
                    },
                    {
                        "role": "user",
                        "content": "I will give you the following email address for analysis: Y8q1iHh.voi70I7.Y8q1iHh@fgdjdyh.onmicrosoft.com\nGive me a percentage of how unusual is the email address"
                    },
                    {
                        "role": "assistant",
                        "content": "probability: 98%. The email address has multiple dots in the local-part and in the domain. The local-part seems to be randomly generated. The domain has a random part followed by a domain related to Microsoft."
                    },  
                    {
                        "role": "user",
                        "content": "Give me a percentage of how professional is the format of the email address"
                    },
                    {
                        "role": "assistant",
                        "content": "probability: 11%. The email address has multiple dots in the local-part that might separate different names, but the names seems to be random generated. The domain has a random part followed by a domain related to Microsoft."
                    },  
                    {
                        "role": "user",
                        "content": "Give me the probability that this email address is spoofed"
                    },
                    {
                        "role": "assistant",
                        "content": "probability: 96%. The email address has multiple dots and random characters. The domain has part that is related to a Microsoft domain."
                    },  
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            case 'subject':
                messages = [
                    {
                        "role": "system",
                        "content": 'You are specialist in phishing detection that always provide a probability that quantifies how the aspect exists in the provided input.'
                    },
                    {
                        "role": "user",
                        "content": "I will give you the following subject header of an email, for analysis: '[Important] Unauthorized access; Your Aܿmܿaܿzܿon account has been locked, Verify your account now. #CASE-ID: 072522.3871922'\nGive me the probability that this subject header is promissing something"
                    },
                    {
                        "role": "assistant",
                        "content": "probability: 12%. The subject header is not promissing anything but informing the user about a potential locked account."
                    },  
                    {
                        "role": "user",
                        "content": "Give me the probability that this subject header is inducing a sense of urgency"
                    },
                    {
                        "role": "assistant",
                        "content": "probability: 90%. The subject header hurries the receiver (Important, now) to verify his/her account because the account was supposedly locked"
                    },  
                    {
                        "role": "user",
                        "content": "Give me the probability that the subject header is inducing a sense of trust for an email"
                    },
                    {
                        "role": "assistant",
                        "content": "percentage: 85%. The subject header impersonates Amazon, which is considered a trustworthy entity"
                    },  
                    {
                        "role": "user",
                        "content": "Give me the probability that the subject header is coming from an authoritative and credible source"
                    },
                    {
                        "role": "assistant",
                        "content": "percentage: 91%. The subject header impersonates Amazon, which is considered a trustworthy entity, and is authoritative to inform its users about their account activity"
                    },  
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
        return messages

    def ask(self, prompt: str, about: str, quiet: bool = False) -> str:
        if len(prompt) > self.CHARACTERS_CHUNK_SIZE:
            prompt = self.get_first_chunk(prompt)
        response = self.client.chat.completions.create(
            model = self.model,
            messages = self.topic_message(about, prompt)
        )
        if quiet:
            return None
        answer = response.choices[0].message.content.strip().split('%')
        self.numeric_answer = float(int(answer[0]) / 100)
        self.explanation = answer[1].strip()
        return list([self.numeric_answer, self.explanation])
