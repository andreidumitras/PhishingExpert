import unicodedata
import feature_parser as ft
import check_lists as lst


def is_replying_to_sender() -> bool:
    return ft.get_reply_address() == ft.get_sender_address()

def is_returning_to_sender() -> bool:
    return ft.get_return_address == ft.get_sender_address()

def is_SPF_passed() -> bool:
    return ft.get_SPF == 'Pass'

def is_popular_email_provider() -> bool:
    sender = ft.get_sender_address()
    email_provider = sender[sender.find('@') + 1:]
    return email_provider in lst.popular_email_services

def has_email_foreign_characters() -> bool:
    sender = ft.get_sender_address()
    for char in sender:
        if char not in '0123456789' and char not in '@._+-~!#$%&/\'=^{}|':
            if not unicodedata.name(char).startswith('LATIN'):
                return True
    return False
    
def get_number_of_receivers() -> float:
    receivers = len(ft.get_receivers())
    max_receivers = 700
    return receivers / max_receivers

def is_encoded() -> bool:
    return ft.get_encoding_status() is not None

def get_number_of_parts() -> float:
    number_of_parts = len(ft.get_parts())
    max_parts = 100
    return number_of_parts / max_parts
    
def has_html() -> bool:
    email_parts = ft.get_parts()
    for part in email_parts:
        if part.content_type.find('html') > -1:
            return True
    return False

def has_images() -> bool:
    email_parts = ft.get_parts()
    for part in email_parts:
        if part.content_type.find('image') > -1:
            return True
    return False

def has_attachments() -> bool:
    email_parts = ft.get_parts()
    for part in email_parts:
        if part.content_type.find('application') > -1:
            return True
    return False

#---------------------

def get_subject_length() -> float:
    subject = ft.get_subject()
    max_length = 988
    return len(subject) / max_length

def is_subject_replied() -> bool:
    subject = ft.get_subject()
    return subject.find('Re: ') > -1

def is_subject_forwarded() -> bool:
    subject = ft.get_subject()
    return subject.find('Fwd: ') > -1

def has_unusual_whitespaces() -> bool:
    subject = ft.get_subject()
    for char in subject:
        if char in lst.unusual_unicode_whitespaces:
            return True
    return False

#---------------------
def get_number_of_words() -> float:
    email_parts = ft.get_parts()
    for part in email_parts:
        if part.content_type == 'text/html':
            
def get_reading_time() -> float:
    
