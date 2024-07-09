import re
import lists

def is_sender_replying_returning_to_itself(addr1: str, addr2: str) -> bool:
    if not addr1 and not addr2:
        return 0
    return int(addr1 == addr2)

def has_sender_address_unrecomended_characters(user: str) -> bool:
    if not user:
        return 0
    # google recomended characters
    pattern = r'[a-zA-Z0-9\-\._]+'
    if not re.fullmatch(pattern, user):
        return 0
    return 1

def is_domanin_common(domain: str) -> bool:
    return int(domain in lists.popular_email_services)

def get_receivers_quotient(number_of_receivers: int) -> float:
    MAX_RECEIVERS = 500
    return number_of_receivers / MAX_RECEIVERS

def is_SPF_passed(status: str) -> bool:
    return int(status.lower() == 'pass')

def get_subject_length_quotient(subject: str) -> float:
    MAX_SUBJECT_LENGTH = 998
    return len(subject) / MAX_SUBJECT_LENGTH

def has_odd_whitespaces(text: str) -> bool:
    for char in text:
        if char in lists.unicode_whitespaces:
            return 1
    return 0

def is_subject_reply(subject: str) -> bool:
    return int('Re: ' in subject)

def is_subject_forwarded(subject: str) -> bool:
    return int('Fwd: ' in subject)

def get_reading_time_quotient(number_of_words: str) -> float:
    AVERAGE_READING_TIME_PER_MINUTE = 200
    MINUTES_IN_AN_HOUR = 60
    return number_of_words / AVERAGE_READING_TIME_PER_MINUTE / MINUTES_IN_AN_HOUR

