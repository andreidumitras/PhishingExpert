import regex
import lists
from difflib import SequenceMatcher

# verify if the provided field exists
def check_for_not_none(content: str | None) -> int:
    return int(content is not None)

# checks if the address1 and address2 are the same or at least similar, and returns the percentage of similarity
def check_for_similarity(str1: str, str2: str) -> float:
    # return the percentage of similarity between the two addresses
    return SequenceMatcher(None, str1, str2).ratio()

def get_length_fraction(content: str) -> float:
    return float(1 / len(content))

# --------------------------- --------------------------- ---------------------------

def has_sender_email_address(sender_address) -> int:
    return check_for_not_none(sender_address)

def has_reply_email_address(reply_address) -> int:
    return check_for_not_none(reply_address)

def has_return_email_address(return_address) -> int:
    return check_for_not_none(return_address)

def has_sender_displayed_name(sender_displayed_name) -> int:
    return check_for_not_none(sender_displayed_name)

def has_reply_displayed_name(reply_displayed_name) -> int:
    return check_for_not_none(reply_displayed_name)

def has_same_email_address(sender, addr) -> float:
    if not sender or not addr:
        return 0
    return check_for_similarity(sender.full, addr.full)
    
def has_displayname_as_email_localpart(display_name, emial_address) -> float:
    if not display_name or not emial_address:
        return 0
    return check_for_similarity(display_name, emial_address.local_part)
    
# checks the list of the top 100 most popular email domains
def has_common_email_domain(email_address) -> int:
    if not email_address:
        return 0
    return int(email_address.domain in lists.popular_email_services)

def get_full_length(content: str) -> float:
    if not content:
        return 0
    return get_length_fraction(content)

def get_displayed_name_length(displayed_name) -> float:
    if not displayed_name:
        return 0
    return float(1 / len(displayed_name))

def get_email_address_length(sender) -> float:
    if not sender:
        return 0
    return float(1 / len(sender.full))

def get_email_address_local_part_length(sender) -> float:
    if not sender:
        return 0
    return float(1 / len(sender.local_part))

def get_email_address_domain_name_length(sender) -> float:
    if not sender:
        return 0
    return float(1 / len(sender.domain))

def get_amount(header: str) -> float:
    if not header:
        return 0
    receivers = header.split(',')
    return 1 / len(receivers)

def pass_spf(spf_status) -> int:
    if not spf_status:
        return 0
    spf = spf_status[0:4]
    return int(spf.lower() == "pass")

# ------------------------------- ------------------------------- -------------------------------
def is_blank(content) -> int:
    return content == None

def has_unusual_characters(subject: str | None) -> int:
    if not subject:
        return 0
    pattern = r"[ -~\p{L}\p{N}\p{P}\p{Sc}\n\r\t]+"
    matches = regex.search(pattern, subject)
    if not matches:
        return 0
    result = matches.group(0)
    return int(result != subject)

def get_number_of_words(subject: str | None) -> float:
    if not subject:
        return 0
    words = subject.count(' ') + 1
    return 1 / words

def get_number_of_digits(subject: str | None) -> float:
    if not subject:
        return 0
    pattern = r"[\d]+"
    numbers = regex.findall(pattern, subject)
    digits = sum(len(n) for n in numbers)
    return 1 / digits

def get_number_of_caps(subject: str | None) -> float:
    if not subject:
        return 0
    caps = sum(ch.isupper() for ch in subject)
    return 1 / caps

def get_number_of_lows(subject: str | None) -> float:
    if not subject:
        return 0
    lows = sum(ch.islower() for ch in subject)
    return 1 / lows
    
def what_is_subject(subject: str | None, isit: str) -> int:
    if not subject:
        return 0
    chunk = subject[0:4].lower()
    return int(isit in chunk)
    
# -------------------------- -------------------------- --------------------------  
def is_text_blank(text: str) -> int:
    return int(text == "")

def is_text_html(html: bool) -> int:
    return int(html == True)

def get_html_number_of_headings(soup) -> float:
    headings = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    number_of_headings = len(soup.find_all(headings))
    if number_of_headings == 0:
        return 0
    return 1 / number_of_headings

def get_html_number_of_paragraphs(soup) -> float:
    paragraphs = len(soup.find_all('p'))
    if paragraphs == 0:
        return 0
    return 1 / paragraphs

def get_html_number_of_links(links: list) -> float:
    number = len(links)
    if number == 0:
        return 0
    return 1 / number

def get_html_number_of_distinct_links(links: list) -> float:
    number = len(set(links))
    if number == 0:
        return 0
    return 1 / number

def get_html_number_of_mailto(links: list) -> float:
    number = 0
    for link in links:
        if "mailto" in link['href']:
            number += 1
    if number == 0:
        return 0
    return 1 / number

def get_html_number_of_http(links: list) -> float:
    number = 0
    for link in links:
        if "http" in link['href']:
            number += 1
    if number == 0:
        return 0
    return 1 / number

def get_html_number_of_images(soup) -> float:
    images = len(soup.find_all('img', src=True))
    if images == 0:
        return 0
    return 1 / images

def get_html_number_of_buttons(soup) -> float:
    buttons = len(soup.find_all('button', src=True))
    if buttons == 0:
        return 0
    return 1 / buttons


def get_html_number_of_scripts(soup) -> float:
    scripts = len(soup.find_all('script', src=True))
    if scripts == 0:
        return 0
    return 1 / scripts


def get_number_or_words(text) -> float:
    if text.strip(" \n\r") == "":
        return 0
    number = text.count(' ') + 1
    return 1 / number


def get_number_or_words(text) -> float:
    if text.strip(" \n\r") == "":
        return 0
    number = len(text)
    return 1 / number


def get_plain_number_of_paragraphs(text: str) -> float:
    matches = regex.findall("\n\n", text)
    if not matches:
        return 0
    return 1 / len(matches)

def get_plain_number_of_links(links: list) -> float:
    if len(links) == 0:
        return 0
    return 1 / len(links)

def get_plain_number_of_distinct_links(links: list) -> float:
    if len(links) == 0:
        return 0
    return 1 / len(set(links))

def get_plain_number_of_mailto(links: list) -> float:
    number = 0
    pattern = r"[\w\-\.\+]+@[\w\.\-]+"
    for link in links:
        matches = regex.search(pattern, link)
        if not matches:
            continue
        number += 1
    if number == 0:
        return 0
    return 1 / number

def get_plain_number_of_http(links: list) -> float:
    number = 0
    for link in links:
        if "http" in link or "www." in link:
            number += 1
    if number == 0:
        return 0
    return 1 / number


# ---------------------------------- ATTACHMENTS ----------------------------------
def get_number_of_attachments(attachments: list) -> int:
    number = len(attachments)
    if number == 0:
        return 0
    return 1 / number
    
def get_number_of_inlines(inlines: list) -> int:
    number = len(inlines)
    if number == 0:
        return 0
    return 1 / number

def get_variety(attachments: list) -> int:
    if len(attachments) == 0:
        return 0
    extensions = set()
    for attachment in attachments:
        info = attachment.split('.')
        if len(info) < 2:
            extensions.add("")
        elif len(info) > 2:
            extensions.add(info[-1])
        else:
            extensions.add(info[1])
    number = len(extensions)
    return 1 / number
