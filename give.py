import sys
from email import policy                # import modulul "email", de unde am importat submodulul  "policy"
from email.parser import BytesParser    # import modul "email" si submodulul "parser", din care am importat clasa BytesParser
from bs4 import BeautifulSoup
import quopri

def extract_html(payload):
    # payload = part.get_payload(decode=True)
    print(payload)


def extract_plain(part):
    pass

def handle_multipart(eml_message) -> list:
    plain_payload = None
    html_payload = None
    for part in eml_message.walk():
        content_type = part.get_content_type()
        if content_type == "text/html":
            print("HTML payload -----------------------------------------------------")
            html_payload = part.get_payload(decode=True)
            # decoded_html_payload = quopri.decodestring(html_payload).decode('Windows-1252')
            charset = part.get_content_charset()
        
            # print(html_payload.decode(encoding=charset, errors="replace"))
            soup = BeautifulSoup(html_payload.decode(encoding=charset, errors="replace"), 'html.parser')
            paragraphs = [tag.get_text() for tag in soup.find_all('p')]
            i = 0
            for p in paragraphs:
                print(f"p[{i}]: {p}")
                i += 1
            # soup = BeautifulSoup(decoded_html_payload, 'html.parser')
            # print(soup.get_text(separator='\n').strip())
        if content_type == "text/plain":
            print("plain payload -----------------------------------------------------")
            plain_payload = part.get_payload(decode=True)
            charset = part.get_content_charset()
            print(plain_payload.decode(encoding=charset, errors="replace"))
    print("+++++++++++++++++++done++++++++++++++++++++++++++")
            
        
# def handle_singlepart(eml_message) -> list:
#     for part in eml_message.walk():
        

if __name__ == "__main__":
    eml_file = sys.argv[1]
    with open(eml_file, 'rb') as eml_handle:
        eml_message = BytesParser(policy=policy.default).parse(eml_handle)
        
    if eml_message.is_multipart():
        handle_multipart(eml_message)
    else:
        handle_singlepart(eml_message)