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

    
def get_number_of_receivers(eml_object) -> int:
    header = eml_object.get("To")
    if not header:
        return None
    return len(header.split(','))

def get_SPF_status(eml_object) -> str:
    status = eml_object.get('Received-SPF')
    if not status:
        return 'None'
    return status[0:4]

def get_subject(eml_object) -> str:
    return eml_object.get('Subject')

def get_number_of_words(text: str) -> int:
    if text:
        return (len(text.split()))
    return 0

def get_text(eml_object) -> list[str]:
    text = None
    filename = None
    if eml_object.is_multipart():
        for part in eml_object.walk():
            content_type = part.get("Content-Type")
            if not content_type:
                return list([None, None])
            if 'text/html' in content_type:
                text = part.get_payload(decode=True)
                if text:
                    if 'charset' in content_type:
                        results = content_type.split(';')
                        index = 0
                        for i in range(len(results)):
                            if 'charset' in results[i]:
                                index = i
                                break
                        charset = results[index].strip().split('=')[1].strip('"')
                        text_html = text.strip().decode(encoding=charset, errors="replace")
                    else:
                        text_html = text.strip().decode(errors="replace")
                    html_parser = html2text.HTML2Text()
                    html_parser.ignore_links = False
                    text = html_parser.handle(text_html)
                # else:
                #     return None
                        
            elif 'text/plain' in content_type:
                text = part.get_payload(decode=True)
                if text:
                    if 'charset' in content_type:
                        results = content_type.split(';')
                        index = 0
                        for i in range(len(results)):
                            if 'charset' in results[i]:
                                index = i
                                break
                        charset = results[index].strip().split('=')[1].strip('"')
                        text = text.strip().decode(encoding=charset, errors="replace")
                    else:
                        text = text.strip().decode(errors="replace")
                # else:
                #     return None
            elif 'application' in content_type and '=' in content_type:
                filename = content_type.split('=')[-1].strip('"')
    else:
        content_type = eml_object.get("Content-Type")
        if not content_type:
            return list([None, None])
        if 'text/html' in content_type:
            text = eml_object.get_payload(decode=True)
            if text:
                if 'charset' in content_type:
                    results = content_type.split(';')
                    index = 0
                    for i in range(len(results)):
                        if 'charset' in results[i]:
                            index = i
                            break
                    charset = results[index].strip().split('=')[1].strip('"')
                    # print('>>>>>>>>>>>>>CHARSET:', results)
                    text_html = text.strip().decode(encoding=charset, errors="replace")
                    
                else:
                    text_html = text.strip().decode(errors="replace")
                html_parser = html2text.HTML2Text()
                html_parser.ignore_links = False
                text = html_parser.handle(text_html)
            # else:
            #     return None
                        
        elif 'text/plain' in content_type:
            text = eml_object.get_payload(decode=True)
            if text:
                if 'charset' in content_type:
                    results = content_type.split(';')
                    index = 0
                    for i in range(len(results)):
                        if 'charset' in results[i]:
                            index = i
                            break
                    charset = results[index].strip().split('=')[1].strip('"')
                    text = text.strip().decode(encoding=charset, errors="replace")
                else:
                    text = text.strip().decode(errors="replace")   
            # else:
            #     return None
    # if re.match(r'^\s*$', text):
    filtered = filter(lambda x: not re.match(r'\n|\t|\r', x), text)
    text = "".join(filtered)
    return list([text, filename])
    