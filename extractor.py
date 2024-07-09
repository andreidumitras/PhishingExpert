# from email import policy
# from email.parser import BytesParser
import re
import html2text
from bs4 import BeautifulSoup

# extracts the email address of the sender
def get_sender_address(eml_object) -> str:
    header = eml_object.get("From")
    if not header:
        return None
    address = re.findall('<.+@.+\.[^@]+>', header) or re.findall('.+@.+\.[^@]+', header)
    if not address:
        return None
    address = address[0]
    return address.strip('<>')
    
# extracts the email address for the return path
def get_return_address(eml_object) -> str:
    header = eml_object.get("Return-Path")
    if not header:
        return None
    address = re.findall('<.+@.+\.[.^@]+>', header) or re.findall('.+@.+\.[.^@]+', header)
    if not address:
        return None
    address = address[0]
    return address.strip('<>')
    
# extracts the email address for the reply-to
def get_reply_address(eml_object) -> str:
    header = eml_object.get("Reply-To")
    if not header:
        return None
    address = re.findall('<.+@.+\..+>', header) or re.findall('.+@.+\..+', header)
    if not address:
        return None
    address = address[0]
    return address.strip('<>')

    
def get_number_of_receivers(eml_object) -> int:
    header = eml_object.get("To")
    if not header:
        return None
    return len(header.split(','))

def get_SPF_status(eml_object) -> str:
    status = eml_object.get('Received-SPF')
    return status[0:4]

def get_subject(eml_object) -> str:
    return eml_object.get('Subject')

def get_number_of_words(text: str) -> int:
    if text:
        return (len(text.split()))
    return None

def get_text(eml_object) -> str:
    text = None
    if eml_object.is_multipart():
        for part in eml_object.walk():
            content_type = part.get("Content-Type")
            if 'text/html' in content_type:
                text = part.get_payload(decode=True)
                if text:
                    charset = content_type.split(';')[1].strip().split('=')[1].strip('"')
                    text_html = text.strip().decode(encoding=charset, errors="replace")
                    html_parser = html2text.HTML2Text()
                    html_parser.ignore_links = False
                    text = html_parser.handle(text_html)
                else:
                    return None
                        
            elif 'text/plain' in content_type:
                text = part.get_payload(decode=True)
                if text:
                    charset = content_type.split(';')[1].strip().split('=')[1].strip('"')
                    text = text.strip().decode(encoding=charset, errors="replace")
                else:
                    return None
                
    else:
        content_type = eml_object.get("Content-Type")
        if 'text/html' in content_type:
            text = eml_object.get_payload(decode=True)
            if text:
                charset = content_type.split(';')[1].strip().split('=')[1].strip('"')
                text_html = text.strip().decode(encoding=charset, errors="replace")
                html_parser = html2text.HTML2Text()
                html_parser.ignore_links = False
                text = html_parser.handle(text_html)
            else:
                return None
                        
        elif 'text/plain' in content_type:
            text = eml_object.get_payload(decode=True)
            if text:
                charset = content_type.split(';')[1].strip().split('=')[1].strip('"')
                text = text.strip().decode(encoding=charset, errors="replace")
            else:
                return None
    return text
    