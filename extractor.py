import regex
from email_address import EmailAddress

# extracts the email address from the sender's string or other envelope header
# extracts the displayed name from the sender's string or other envelope header
# returns a list with the displayed name and with the email address
def get_email_address_and_displayed_name_data(content: str) -> list:
    if not content:
        return list([None, None])
    # email address extraction
    # regex to match the last email address that might be enclosed between < >
    email_address_pattern = r"<?[\w\-\.\+@=]+@[\w\.\-]+>?$"
    # if content is too long, impose a limit of 1000 characters and trim the string
    if len(content) > 1000:
        content = content[:1000]
        # modify the regex to match any email address, not just the last
        email_address_pattern = r"<?[\w\-\.\+@=]+@[\w\.\-]+>?"
        
    matches = regex.search(email_address_pattern, content)
    if matches:
        sender_address = EmailAddress(matches.group(0).strip('<>'))
    else:
        sender_address = None
    # displayed name extraction
    displayed_name = regex.split(email_address_pattern, content)[0].strip()
    if displayed_name == '':
        displayed_name = None
    return list([displayed_name, sender_address])

# extract the text payload
# extract the HTML flag
# extract the inline resources by the filename (images and others)
# extract the attachments (filenames)
# returns a list composed from all of these
def get_email_payloads(eml) -> list:
    inlines = []
    attachments = []
    text_html = None
    text_plain = None
    is_html = False
    if eml.is_multipart():
        for part in eml.walk():
            content_type = part.get_content_type()
            if content_type == "text/html":
                is_html = True
                # payload is encoded (base64, quoted-printable, 7bit, 8bit)
                html_payload = part.get_payload(decode=True)
                charset = part.get_content_charset()
                if not charset:
                    text_html = html_payload.decode(errors="replace")
                else:
                    text_html = html_payload.decode(encoding=charset, errors="replace")                    
            elif content_type == "text/plain":
                plain_payload = part.get_payload(decode=True)
                charset = part.get_content_charset()
                if not charset:
                    text_plain = plain_payload.decode(errors="replace")
                else:
                    text_plain = plain_payload.decode(encoding=charset, errors="replace")
            content_disposition = part.get_content_disposition()
            if not content_disposition:
                continue
            full = part.get("Content-Disposition")
            filename_pattern = r"\"[\w\s\.\+\-'=;,?!~\(\)\[\]\{\}]+\""
            matches = regex.search(filename_pattern, full)
            if not matches:
                continue
            filename = matches.group(0).strip('\"')
            if content_disposition == "inline":
                inlines.append(filename)
            elif content_disposition == "attachment":
                attachments.append(filename)
    else:
        content_type = eml.get_content_type()
        if content_type == "text/html":
            is_html = True
            html_payload = eml.get_payload(decode=True)
            charset = eml.get_content_charset()
            if not charset:
                text_html = html_payload.decode(errors="replace")
            else:
                text_html = html_payload.decode(encoding=charset, errors="replace")
        elif content_type == "text/plain":
            plain_payload = eml.get_payload(decode=True)
            charset = eml.get_content_charset()
            if not charset:
                text_plain = plain_payload.decode(errors="replace")
            else:
                text_plain = plain_payload.decode(encoding=charset, errors="replace")
            content_disposition = eml.get_content_disposition()

    if text_html:
        return list([text_html, is_html, inlines, attachments])
    elif text_plain:
        return list([text_plain, is_html, inlines, attachments])
    return list([None, None, inlines, attachments])

# extract text from HTML payload using BeautifulSoup
# and getting rid of the extra new lines and carrige return characters
# returns a string will all the text
def get_html_text_content(soup) -> str:
    text = soup.get_text()
    return regex.sub(r"([\n]{2,}|\r+)", "\n", text)

# extract all the hyperlink references from the a tags, using BeautifulSoup
# hyperlinks were considered to be only from a tags
# returns a list with all the URLS
def get_html_hyperlinks(soup) -> list:
    links = soup.find_all('a', href=True)
    return links

# extract plain text from a plain payload
# and getting rid of the extra new lines and carrige return characters
# returns a string will all the text
def get_plain_text_content(payload: str) -> str:
    return regex.sub(r"([\n]{2,}|\r+)", "\n", payload)

# extracting anything that can be an URL using regex
# returns a list with all the URLS
def get_plain_hyperlinks(text) -> list:
    urlpattern = r"(?:http[s]?:\/\/.)?(?:www\.)?[-a-zA-Z0-9@%._\+~#]{2,256}\.[a-z]{2,6}\b(?:[-a-zA-Z0-9@:%_\+.~#?&\/\/=]*)"
    matches = regex.findall(urlpattern, text)
    if not matches:
        return list([])
    return matches
