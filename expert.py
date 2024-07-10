from openai import OpenAI
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter

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
            chunc_size = self.CHARACTERS_CHUNK_SIZE,
            chunk_overlap = 0,
            length_function = len,
        )
        chunks = rec_text_splitter.split_text(prompt)
        return chunks[0]

    # def topic_message(self, topic: str, prompt: str):
    #     # NOTE:
    #         #   system:     it modifies the personality of the model
    #         #   user:       the user query
    #         #   assistant:  give examples of desired behaviours
    #         # messages variable gives a short experience for the model in order to answer properly.
    #     match topic:
    #         case 'email_address':        
    #             messages = [
    #                 {
    #                     "role": "system",
    #                     "content": 'You are specialist in phishing detection that always provide a probability that quantifies how the aspect exists in the provided input. You will always answer with percentages to all the requests.'
    #                 },
    #                 {
    #                     "role": "user",
    #                     "content": "I will give you the following email address for analysis: Y8q1iHh.voi70I7.Y8q1iHh@fgdjdyh.onmicrosoft.com\nGive me a percentage of how unusual is the email address"
    #                 },
    #                 {
    #                     "role": "assistant",
    #                     "content": "probability: 98%. The email address has multiple dots in the local-part and in the domain. The local-part seems to be randomly generated. The domain has a random part followed by a domain related to Microsoft."
    #                 },  
    #                 {
    #                     "role": "user",
    #                     "content": "Give me a percentage of how professional is the format of the email address"
    #                 },
    #                 {
    #                     "role": "assistant",
    #                     "content": "probability: 11%. The email address has multiple dots in the local-part that might separate different names, but the names seems to be random generated. The domain has a random part followed by a domain related to Microsoft."
    #                 },  
    #                 {
    #                     "role": "user",
    #                     "content": "Give me the probability that this email address is spoofed"
    #                 },
    #                 {
    #                     "role": "assistant",
    #                     "content": "probability: 96%. The email address has multiple dots and random characters. The domain has part that is related to a Microsoft domain."
    #                 },  
    #                 {
    #                     "role": "user",
    #                     "content": prompt
    #                 }
    #             ]
    #         case 'subject':
    #             messages = [
    #                 {
    #                     "role": "system",
    #                     "content": 'You are specialist in phishing detection that always provide a probability that quantifies how the aspect exists in the provided input. You will always answer with percentages to all the requests.'
    #                 },
    #                 {
    #                     "role": "user",
    #                     "content": "I will give you the following subject header of an email, for analysis: '[Important] Unauthorized access; Your Aܿmܿaܿzܿon account has been locked, Verify your account now. #CASE-ID: 072522.3871922'\nGive me the probability that this subject header is promissing something"
    #                 },
    #                 {
    #                     "role": "assistant",
    #                     "content": "probability: 12%. The subject header is not promissing anything but informing the user about a potential locked account."
    #                 },  
    #                 {
    #                     "role": "user",
    #                     "content": "Give me the probability that this subject header is inducing a sense of urgency"
    #                 },
    #                 {
    #                     "role": "assistant",
    #                     "content": "probability: 90%. The subject header hurries the receiver (Important, now) to verify his/her account because the account was supposedly locked"
    #                 },  
    #                 {
    #                     "role": "user",
    #                     "content": "Give me the probability that the subject header is inducing a sense of trust for an email"
    #                 },
    #                 {
    #                     "role": "assistant",
    #                     "content": "probability: 85%. The subject header impersonates Amazon, which is considered a trustworthy entity"
    #                 },  
    #                 {
    #                     "role": "user",
    #                     "content": "Give me the probability that the subject header is coming from an authoritative and credible source"
    #                 },
    #                 {
    #                     "role": "assistant",
    #                     "content": "probability: 91%. The subject header impersonates Amazon, which is considered a trustworthy entity, and is authoritative to inform its users about their account activity"
    #                 },  
    #                 {
    #                     "role": "user",
    #                     "content": "Give me the percentage of how suspicious is the structure of this header"
    #                 },
    #                 {
    #                     "role": "assistant",
    #                     "content": "probability: 88%. The subject header impersonates Amazon but it contains some non-ASCII, barely visible characters between the letters of 'Amazon' word which is not normal"
    #                 },  
    #                 {
    #                     "role": "user",
    #                     "content": prompt
    #                 }
    #             ]
    #         case 'text':
    #             messages = [
    #                 {
    #                     "role": "system",
    #                     "content": 'You are specialist in phishing detection that always provide a probability that quantifies how the aspect exists in the provided input. You will always answer with percentages to all the requests.'
    #                 },
    #                 {
    #                     "role": "user",
    #                     "content": "I will give you the following text of an email, for analysis. Focus of the phrases, because it contains some URLs:\n[![Trustwallet Logo](https://apps.uk/wp-content/uploads/2021/11/metamask-trust-wallet.jpg)](http://www.thinkific.com)  ---  |  | ###  Hi Dear; phishing@pot    ---  All unverified accounts will be suspended on 10/31/2022.  We're sorry for any inconvenience we cause with this, but please keep in mindthat our intention is to keep our customers safe and happy.  [Confirm my wallet](https://usertest.sciquest.com/apps/Router/ExternalSiteTransition?url=https://drop-coin-availablenow.site44.com/)    Thanks for doing that!  Trustwallet Team  [GetHelp](https://usertest.sciquest.com/apps/Router/ExternalSiteTransition?url=https://drop-coin-availablenow.site44.com/)   [ ContactUs](mailto:customers@Trustwallet.com)  **    qckztlefgd630ihmb87japyn254woxvuqckztlefgd630ihmb87japyn254woxvuqckztlefgd630ihmb87japyn254woxvu."
    #                 },
    #                 {
    #                     "role": "assistant",
    #                     "content": "ok, let's see."
    #                 },  
    #                 {
    #                     "role": "user",
    #                     "content": "Give me the probability that other people are mentioned in this text"
    #                 },
    #                 {
    #                     "role": "assistant",
    #                     "content": "probability: 70%. The email ensures the user that they try to keep 'our customers happy' and speaks of others 'all unverified accounts'"
    #                 },  
    #                 {
    #                     "role": "user",
    #                     "content": "Give me the probability that this text convey a sense of urgency"
    #                 },
    #                 {
    #                     "role": "assistant",
    #                     "content": "probability: 21%. The text is kindly suggesting to the receiver to 'Confirm my wallet'"
    #                 },  
    #                 {
    #                     "role": "user",
    #                     "content": "Give me the percentage of the authoritative tone"
    #                 },
    #                 {
    #                     "role": "assistant",
    #                     "content": "probability: 15%. The tone of the email is chill and informative"
    #                 },  
    #                 {
    #                     "role": "user",
    #                     "content": "Give me the percentage of the flattery present in the email text and how much it tries to connect with the receiver"
    #                 },
    #                 {
    #                     "role": "assistant",
    #                     "content": "probability: 63%. The email starts with 'hi dear', trying to connect emotionally wirh the receiver. They thank the receiver 'thank you for doing that'"
    #                 },  
    #                 {
    #                     "role": "user",
    #                     "content": "Give me the percentage of how clear is that the receiver have to do something"
    #                 },
    #                 {
    #                     "role": "assistant",
    #                     "content": "probability: 23%. The text sais that the receiver can visit his wallet, without any other instruction"
    #                 },  
    #                 {
    #                     "role": "user",
    #                     "content": "Give me the percentage of how clear is that there is a reward or an enticing offer for the receiver"
    #                 },
    #                 {
    #                     "role": "assistant",
    #                     "content": "probability: 4%. The text is not mentioning any offer but something that the receiver can take into consideration"
    #                 },  
    #                 {
    #                     "role": "user",
    #                     "content": "Give me a percentage of how professional is the structure of the email"
    #                 },
    #                 {
    #                     "role": "assistant",
    #                     "content": "probability: 34%. The text has a more personal tone rather than a professional one"
    #                 },
    #                 {
    #                     "role": "user",
    #                     "content": "Give me a percentage of how personalized is the email"
    #                 },
    #                 {
    #                     "role": "assistant",
    #                     "content": "probability: 63%. The text has more a personal but is does not mention any personal information regarding the receiver"
    #                 },
    #                 {
    #                     "role": "user",
    #                     "content": "Give me a percentage of how vague is the tone and the content of the given email"
    #                 },
    #                 {
    #                     "role": "assistant",
    #                     "content": "probability: 70%. The text si vague because it mentions that the user's account will be suspended and not providing any reason"
    #                 },
    #                 {
    #                     "role": "user",
    #                     "content": "Give me a percentage that suggests how much the text is talking about user\'s personal information; like credit cards, passwords, accounts or a billing address"
    #                 },
    #                 {
    #                     "role": "assistant",
    #                     "content": "probability: 84%. The email mentions a 'wallet' confirmation request for the receiver"
    #                 },
    #                 {
    #                     "role": "user",
    #                     "content": "Give me the percentage of how plausible is the narrative"
    #                 },
    #                 {
    #                     "role": "assistant",
    #                     "content": "probability: 19%. The email's narrative seems to be invented, without any concrete detail and reason behind, only for the user to reveal his credentials"
    #                 },
    #                 {
    #                     "role": "user",
    #                     "content": "Give me the probability that the following text is containing grammatical errors"
    #                 },
    #                 {
    #                     "role": "assistant",
    #                     "content": "probability: 40%. The email has 2 words concatenated 'mindthat'"
    #                 },
    #                 {
    #                     "role": "user",
    #                     "content": "Give me a percentage of how suspicious are all the URLs mentioned in the email"
    #                 },
    #                 {
    #                     "role": "assistant",
    #                     "content": "probability: 100%. The email has URLs embedded inside anotehr URLs ('https://usertest.sciquest.com/apps/Router/ExternalSiteTransition?url=https://drop-coin-availablenow.site44.com/')"
    #                 },
    #                 {
    #                     "role": "user",
    #                     "content": "Give me a percentage of how suspicious for phishing is this site"
    #                 },
    #                 {
    #                     "role": "assistant",
    #                     "content": "probability: 100%. The email has URLs embedded inside anotehr URLs, vague information, grammatical problems and others cues for phishing"
    #                 },
    #                 {
    #                     "role": "user",
    #                     "content": prompt
    #                 }
    #             ]
                
    #     return messages

    def ask(self, prompt: str, quiet: bool = False) -> list[float]:
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
        pattern = re.compile('\d%')
        result = pattern.search(answer)
        return result.group(1)
        # return answer
