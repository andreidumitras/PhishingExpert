import phishing_researcher as phish
from bs4 import BeautifulSoup
import base64
import quopri
import html2text
import re

class Part(object):
    def __init__(self, content_type, encoding, payload):
        self.content_type = content_type
        self.encoding = encoding
        # in case of attachment, it will be the filename.
        self.payload = payload
        
    def get_payload(self) -> str:
        return self.payload
    
    def get_content_type(self) -> str:
        return self.content_type
    
    def get_encoding(self) -> str:
        return self.encoding
    
    def decode_payload(self) -> str:
        text = ''''''
        if self.content_type.find('text') != -1:
            match self.encoding:
                case 'base64':
                    text = str(base64.b64decode(self.payload))
                case 'quoted‑printable':
                    text = str(quopri.decodestring(self.payload))
                case '8bit':
                    try:
                        text = self.payload.decode('utf-8')
                    except UnicodeDecodeError:
                        text = self.payload.decode('latin1')
                case '7bit':
                    text = self.payload.decode('ascii')
                case 'binary':
                    text = self.payload
            return text
        return None
    
    def extract_html_text(self) -> str:
        html_content = html2text.HTML2Text()
        html_content.ignore_links = False
        return html_content.handle(self.decode_payload())
    
    def get_file_name(self) -> str:
        start = self.payload.find('"')
        if start != -1:
            stop = self.payload.rfind('"')
            filename = self.payload[start + 1:stop]
        else:
            start = self.payload.find('=')
            filename = self.payload[start + 1:]
        return filename.strip()
        
    def show(self):
        print('------------------- inceput parte ------------------')
        print('type:', self.content_type, 'encoding:', self.encoding, 'payload:', self.payload)
        print('------------------- sfarsit parte ------------------')

# get the email address from the From header
def get_sender_address() -> str:
    from_header = phish.email_file.get('From')
    start = from_header.find('<')
    if start != -1:
        from_header = from_header[start + 1:]
        from_header = from_header.rstrip('>')
    return from_header.strip()
    
# get the email address from the Return-Path header
def get_return_address() -> str:
    return_header = phish.email_file.get('Return-Path')
    if return_header is None:
        return None
    start = return_header.find('<')
    if start != -1:
        return_header = return_header[start + 1:]
        return_header = return_header.rstrip('>')
    return return_header.strip()
    
# get the email address from the Reply-To header
def get_reply_address() -> str:
    reply_header = phish.email_file.get('Reply-To')
    if reply_header is None:
        return None
    start = reply_header.find('<')
    if start != -1:
        reply_header = reply_header[start + 1:]
        reply_header = reply_header.rstrip('>')
    return reply_header.strip()
    
# get the SPF status from the Received-SPF header
def get_SPF_status() -> str:
    SPF_status = phish.email_file.get('Received-SPF')
    SPF_status = SPF_status[0:4]
    return SPF_status

# count the list of receivers from the To header, splitted by ','
def count_receivers() -> int:
    to_header = phish.email_file.get('To')
    return len(to_header.split(','))
    
def decode_payload(payload, encodin_algorithm) -> str:
    text = ''
    match encodin_algorithm:
        case 'base64':
            text = str(base64.b64decode(payload))
        case 'quoted‑printable':
            text = str(quopri.decodestring(payload))
        case '8bit':
            # try:
            #     text = str(payload, encoding='utf-8')
            # except UnicodeEncodeError:
            text = str(payload, encoding='latin-1')
        case '7bit':
            text = str(payload, encoding='ascii')
        case 'binary':
            text = str(payload, encoding='latin-1')
    return text

def extract_text_from_html(payload) -> str:
    text_extractor = html2text.HTML2Text()
    text_extractor.ignore_links = True
    return text_extractor.handle(payload)

def extract_urls_from_text(payload) -> list[str]:
    tokens = payload.split()
    urls = []
    for token in tokens:
        if token.startswith('https:') or token.startswith('http:') or token.startswith('ftp'):
            urls.append(token)
    return urls

def extract_urls_from_html(payload) -> list[str]:
    urls = []
    soup = BeautifulSoup(payload, 'html.parser')
    for url in soup.find_all('a'):
        urls.append(str(url.get('href')))
    for url in soup.find_all('img'):
        urls.append(str(url.get('href')))
    return urls

def get_attachment_filename(string) -> str:
    start = string.find('"')
    end = string[start + 1:].find('"')
    return string[start + 1:end]

def verify_scripts(payload) -> bool:
    soup = BeautifulSoup(payload, 'html.parser')
    return len(soup.find_all('script')) != 0
    

def get_text_urls_and_flags() -> list:
    result = []
    urls = []
    payload = b''
    has_image = False
    has_attachment = False
    is_encoded = False    
    has_html = False
    has_scripts = False
    content_type = phish.email_file.get('Content-Type')
    if 'multipart' in content_type:
        for part in phish.email_file.walk():
            _type = part.get_content_type()            
            if 'text' in _type:
                payload = bytes(part.get_payload(), encoding='utf-8')
                print(type(payload))
                encoding_method = part.get('Content-Transfer-Encoding')
                if encoding_method:
                    is_encoded = True
                    payload = decode_payload(payload, encoding_method)
                if 'html' in _type:
                    has_html = True
                    has_scripts = verify_scripts(payload.lower())
                    urls = extract_urls_from_html(payload)
                    payload = extract_text_from_html(payload)
                else:
                    urls = extract_urls_from_text(payload)
            elif 'image' in _type:
                has_image = True
            elif 'application' in _type:
                has_attachment = True
                filename = part.get('Content-Type')
                filename = get_attachment_filename(filename)                
    elif 'text' in content_type:
        payload = bytes(phish.email_file.get_payload(), encoding='utf-8')
        encoding_method = phish.email_file.get('Content-Transfer-Encoding')
        if encoding_method:
            is_encoded = True
            payload = decode_payload(payload, encoding_method)
        if 'html' in content_type:
            has_html = True
            has_scripts = verify_scripts(payload.lower())
            urls = extract_urls_from_html(payload)
            payload = extract_text_from_html(payload)
        else:
            urls = extract_urls_from_text(payload)
    result = [payload, [is_encoded, has_attachment, has_html, has_image, has_scripts], urls]
    return result

def get_subject() -> str:
    subject_header = phish.email_file.get('Subject')
    return subject_header

def get_encoding_status() -> str:
    return phish.email_file.get('Content-Transfer-Encoding')



if __name__ == "__main__":

    # print("From: ", get_sender_address())
    # print("Return-Path: ", get_return_address())
    # print("Reply-To: ", get_reply_address())
    # print("Received-SPF: ", get_SPF())
    # print("Receivers (To): ")
    # [print('->', x) for x in get_receivers()]
    
    # print("Parts: ")
    # [x.show() for x in get_parts()]
    
    # print("Subject:", get_subject())
    print(get_text_urls_and_flags()[0])
    

