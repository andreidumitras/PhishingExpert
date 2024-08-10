import regex
from email import policy                    # for reading emails
from email.parser import BytesParser        # for reading emails
# from email import policy                    # for reading emails
# from email.parser import BytesParser        # for reading emails
import sys
import extractor
import detective
# from email_address import EmailAddress
from bs4 import BeautifulSoup

# # def get_from_data(content: str) -> list:
# #     # regex to match the last email address that might be enclosed between < >
# #     email_address_pattern = r"<?[\w\-\.\+@=]+@[\w\.\-]+>?$"
# #     # if content is too long, impose a limit of 1000 characters and trim the string
# #     if len(content) > 1000:
# #         content = content[:1000]
# #         # modify the regex to match any email address, not just the last
# #         email_address_pattern = r"<?[\w\-\.\+@=]+@[\w\.\-]+>?"
        
# #     matches = regex.search(email_address_pattern, content)
# #     if matches:
# #         sender_address = EmailAddress(matches.group(0).strip('<>'))
# #     else:
# #         sender_address = None
# #     print(matches)
# #     displayed_name = regex.split(email_address_pattern, content)[0]
# #     if displayed_name == '':
# #         displayed_name = None
# #     return list([displayed_name, sender_address])


def read_email(filename: str) -> str:
    with open(filename, 'rb') as emlhandle:
        emlobject = BytesParser(policy = policy.default).parse(emlhandle)
    result = extractor.get_email_payloads(emlobject)

    payload = result[0]
    # else:
        # payload = other
    if result[1]:
        soup = BeautifulSoup(payload, 'html.parser')
        # print(soup.prettify())
        text = extractor.get_html_text_content(soup)
        print(text)
        hyperlinks = extractor.get_html_hyperlinks(soup)
        print("Number of headings", detective.get_html_number_of_headings(soup))
        print("Number of paragraphs", detective.get_html_number_of_paragraphs(soup))
        print("Number of links", detective.get_html_number_of_links(hyperlinks))
        print("Number of distinct links", detective.get_html_number_of_distinct_links(hyperlinks))
        print("Number of httpes", detective.get_html_number_of_http(hyperlinks))
        print("Number of mailtos", detective.get_html_number_of_mailto(hyperlinks))
        print("Number of images", detective.get_html_number_of_images(soup))
        print("Number of buttons", detective.get_html_number_of_buttons(soup))
        print("Number of scripts", detective.get_html_number_of_scripts(soup))
        print("Number of unusual html", detective.has_unusual_characters(text))
        
    else:
        text = extractor.get_plain_text_content_stripped(payload)
        print(text)
        hyperlinks = extractor.get_plain_hyperlinks(payload)
        print("Number of paragraphs", detective.get_plain_number_of_paragraphs(text))
        print("Number of links", detective.get_plain_number_of_links(hyperlinks))
        print("Number of distinct links", detective.get_plain_number_of_distinct_links(hyperlinks))
        print("Number of httpes", detective.get_plain_number_of_http(hyperlinks))
        print("Number of mailtos", detective.get_plain_number_of_mailto(hyperlinks))
        print("Number of unusual plain", detective.has_unusual_characters(text))
    
    # print(text)
def get_plain_text_content(payload: str) -> str:
    return regex.sub(r"[\r]+", "", payload)


if __name__ == "__main__":
    # emlfile = sys.argv[1]
    # with open(emlfile, 'rb') as emlhandle:
    #     emlobject = BytesParser(policy = policy.default).parse(emlhandle)
    # print(emlobject.get("Return-Path"))
    
    # read_email(sys.argv[1])
    import openai

# Replace 'your-api-key' with your actual OpenAI API key
openai.api_key = 'lm-studio'

# Define the model you want to use
model = 'text-davinci-003'  # You can change this to another model like 'text-curie-001' if desired

# Define the prompt
prompt = "Write a poem about the sea."

# Query the model
response = openai.Completion.create(
    engine=model,
    prompt=prompt,
    max_tokens=150,  # Adjust the number of tokens as needed
    n=1,  # Number of completions to generate
    stop=None,  # Define a stopping sequence if needed
    temperature=0.7  # Adjust the temperature for creativity
)

# Print the response
print(response.choices[0].text.strip())
    # text = '''dubill hd7t invited you to view a collectionIn regards to that Go to form https://docs.google.com/forms/d/e/1FAIpQLSfGJfSDGslMI1OQ1x_pcUzzvvmvoqm5MpCDIwtL9d7wZYMoZQ/viewform#1kt5m6bzsbw4r3qlyqntjtr1znxtnr4jywchse🌅 we hope our chosen optBy dubill hd7t · 1 itemView collectionYou received this mail because dubill hd7t shared this collection with you. If you no longer wish to receive email notification of shared collections, unsubscribe here.Get the Google Search App\''''
    # pattern = r"[ -~\p{L}\p{N}\p{P}\p{Sc}\n\r\t]+"
    # matches = regex.search(pattern, text)
    # if not matches:
    #     print("no match")
    # print(matches.group(0))
    # print(matches.group(0) == text)
    # texts = []
    # for element in soup.find_all(string=True):
    #     stripped_text = element.strip()
    #     if stripped_text:  # Exclude empty strings
    #         texts.append(stripped_text)
    # print("ujsdgagadgvkshgvkjghvhjsdfbvlhdbvh")
    # for _ in texts:
    #     print(_)