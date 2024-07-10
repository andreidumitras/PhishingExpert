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
    if address[0].count('@') > 1:
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

# returns the number of receivers from To header
def get_number_of_receivers(eml_object) -> int:
    header = eml_object.get("To")
    if not header:
        return None
    return len(header.split(','))

# returns the first four letters for SPF status (PASS/FAIL/*)
def get_SPF_status(eml_object) -> str:
    status = eml_object.get('Received-SPF')
    if not status:
        return 'None'
    return status[0:4]

# returns the Subject header
def get_subject(eml_object) -> str:
    return eml_object.get('Subject')

# computes the number of words separated by whitespaces
def get_number_of_words(text: str) -> int:
    if text:
        return (len(text.split()))
    return 0

# extract the charset from Content-Type header
def get_charset(content_type: str) -> str:
    results = content_type.split(';')
    index = 0
    for i in range(len(results)):
        if 'charset' in results[i]:
            index = i
            break
    return results[index].strip().split('=')[1].strip('"')

# extract text from HTML format, decoded to be analysed
def get_text_from_html(part, content_type: str) -> str:
    text = part.get_payload(decode=True)
    if not text:
        return None
    if 'charset' in content_type:
        charset = get_charset(content_type)
        text_html = text.strip().decode(encoding=charset, errors="replace")
    else:
        text_html = text.strip().decode(errors="replace")
    html_parser = html2text.HTML2Text()
    html_parser.ignore_links = False
    text = html_parser.handle(text_html)
    return text

# extract the text from plain payload, decoding and preparing it for analysis
def get_text_from_plain(part, content_type: str) -> str:
    text = part.get_payload(decode=True)
    if not text:
        return None
    if 'charset' in content_type:
        charset = get_charset(content_type)
        text = text.strip().decode(encoding=charset, errors="replace")
    else:
       text = text.strip().decode(errors="replace")
    return text

# extract text from an email (multipart/single part)
def get_text(eml_object) -> str:
    text = None
    if eml_object.is_multipart():
        for part in eml_object.walk():
            content_type = part.get("Content-Type")
            if not content_type:
                return None
            if 'text/html' in content_type:
                text = get_text_from_html(part, content_type)
            elif 'text/plain' in content_type:
                text = get_text_from_plain(part, content_type)
    else:
        content_type = eml_object.get("Content-Type")
        if not content_type:
            return None
        if 'text/html' in content_type:
            text = get_text_from_html(eml_object, content_type)        
        elif 'text/plain' in content_type:
            text = get_text_from_plain(eml_object, content_type)

    # get rid of extra new lines, tabs and caridge returns
    filtered = filter(lambda x: not re.match(r'\n|\t|\r', x), text)
    text = "".join(filtered)
    return text
