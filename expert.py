from openai import OpenAI

class Expert:
    def __init__(self):
        self.model: str = None
        # Point to the local serverclient = 
        self.client = OpenAI(base_url = "http://localhost:1234/v1", api_key = "lm-studio")
        self.personality: str = None
        self.numeric_answer: float = None
        self.explanation: str = None

    def ask(self, prompt: str, quiet: bool = False) -> str:
        response = self.client.chat.completions.create(
            model = self.model,
            # NOTE:
            #   system:     it modifies the personality of the model
            #   user:       the user query
            #   assistant:  give examples of desired behaviours
            # messages variable gives a short experience for the model in order to answer properly.
            messages = [
                {
                    "role": "system",
                    "content": self.personality
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        if quiet:
            return None
        if self.explanation:
            answer = response.choices[0].message.content.strip().split('%')
            self.numeric_answer = float(int(answer[0]) / 100)
            self.explanation = answer[1].strip()
            return list([self.numeric_answer, self.explanation])
        
        answer = response.choices[0].message.content.strip().split('%')
        self.numeric_answer = float(int(answer[0]) / 100)
        return self.numeric_answer
