from email import policy
from email.parser import BytesParser
import sys
import extractor
import detective
from expert import Expert

# def construct_explained_vector() -> list:
#     vector = [
#         [detective.is_sender_replying_returning_to_itself(), ]
#     ]

def aff(vector):
    print("Email vector:")
    for i in range(len(vector)):
        print(f'  elem[{i}] = {vector[i]}')
    

if __name__ == "__main__":
    with open(sys.argv[1], 'rb') as eml_file:
        eml_object = BytesParser(policy = policy.default).parse(eml_file)
        
    # print(eml_object.get('Subject'))
    # exit()
    
    sender_address = extractor.get_sender_address(eml_object)
    reply_return_address = extractor.get_return_address(eml_object) or extractor.get_reply_address(eml_object)
    if sender_address:
        split = sender_address.split('@')
        sender_name = split[0]
        sender_domain = split[1]
    else:
        sender_name = None
        sender_domain = None
    number_of_receivers = extractor.get_number_of_receivers(eml_object)
    status_SPF = extractor.get_SPF_status(eml_object)

    subject = extractor.get_subject(eml_object)
    
    text = extractor.get_text(eml_object)
    number_of_words = extractor.get_number_of_words(text)
    
    # load detective observations:
    detective_vector = [
        detective.is_sender_replying_returning_to_itself(sender_address, reply_return_address),
        detective.has_sender_address_unrecomended_characters(sender_name),
        detective.is_domanin_common(sender_domain),
        detective.get_receivers_quotient(number_of_receivers),
        detective.is_SPF_passed(status_SPF),
        detective.get_subject_length_quotient(subject),
        detective.has_odd_whitespaces(subject),
        detective.is_subject_reply(subject),
        detective.is_subject_forwarded(subject),
        detective.get_reading_time_quotient(number_of_words),
        detective.has_odd_whitespaces(text)
    ]
    aff(detective_vector)
    
    # load expert answers
    subject_questions = [
        '',
    ]
    
    expert = Expert()
    expert.model = 'llama'
    expert.personality = 'You are specialist in phishing email recognition. You will provide answers in percentage followed by a short explanation of your reasoning. The response format is "[x%] explanation".'
    print(expert.ask('I will give you the Subject header of an email. Please do not answer yet, only when I will ask you something.'))
    expert.ask(subject)
    for question in subject_questions:
        print(expert.ask(question))
    # content_questions = [
    #     '',
    # ]
    