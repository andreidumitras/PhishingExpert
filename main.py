from email import policy
from email.parser import BytesParser
import sys
import os

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
    # path = '../Datasets/ham/'
    # for eml in os.listdir(path):
    # with open(path + eml, 'rb') as eml_file:
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
    
    result = extractor.get_text(eml_object)
    text = result[0]
    filename = result[1]
    number_of_words = extractor.get_number_of_words(text)
    # print(number_of_words,'------>',eml,'+ file:', filename)
    # exit()
    # load detective observations:
    detective_vector = [
        detective.is_sender_replying_returning_to_itself(sender_address, reply_return_address),
        detective.has_sender_address_unrecomended_characters(sender_name),
        detective.is_domanin_common(sender_domain),
        detective.get_receivers_quotient(number_of_receivers),
        detective.is_SPF_passed(status_SPF),
        detective.is_empty(subject),
        detective.get_subject_length_quotient(subject),
        detective.has_odd_whitespaces(subject),
        detective.is_subject_reply(subject),
        detective.is_subject_forwarded(subject),
        detective.is_empty(text),
        detective.get_reading_time_quotient(number_of_words),
        detective.has_odd_whitespaces(text)
        
    ]
    aff(detective_vector)
    
    
    
    # load expert answers
    # email analysis
    # sender_email_address_requests = [
    #     'Give me a percentage of how unusual is the email address',
    #     'Give me a percentage of how professional is the format of the email address',
    #     'Give me the probability that this email address was spoofed'
    # ]
    # # Gragg's psychological triggers
    # subject_requests = [
    #     'Give me the probability that this subject header is promissing something',
    #     'Give me the probability that this subject header is inducing a sense of urgency',
    #     'Give me the probability that the subject header is inducing a sense of trust for an email',
    #     'Give me the probability that the subject header is coming from an authoritative and credible source',
    #     'Give me the percentage of how suspicious is the structure of this header'
    # ]
    
    # Cialdini's persuasion principles
    # text_requests = [
    #     'Give me the probability that other people are mentioned in this text',
    #     'Give me the probability that this text convey a sense of urgency',
    #     'Give me the percentage of the authoritative tone',
    #     'Give me the percentage of the flattery present in the email text and how much it tries to connect with the receiver',
    #     'Give me the percentage of how clear is that the receiver have to do something',
    #     'Give me the percentage of how clear is that there is a reward or an enticing offer for the receiver',
    #     'Give me a percentage of how professional is the structure of the email',
    #     'Give me a percentage of how personalized is the email',
    #     'Give me a percentage of how vague is the tone and the content of the given email',
    #     'Give me a percentage that suggests how much the text is talking about user\'s personal information; like credit cards, passwords, accounts or a billing address',
    #     'Give me the percentage of how plausible is the narrative',
    #     'Give me the probability that the following text is containing grammatical errors',
    #     'Give me a percentage of how suspicious are all the links mentioned in the email',
    #     'Give me a percentage of how suspicious for phishing is this site'
    # ]
 
    expert_vector = []
    
    expert = Expert()
    expert.model = 'lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF'
    
    # about the sender
    if sender_address:
        ans = expert.ask('I will give you an email address for analysis:' + sender_address, about='email_address')
        print('Email:')
        print(ans)
        # for request in sender_email_address_requests:
        #     expert_vector.append(expert.ask(request, about='email_address')[0])
    else:
        for i in range(3):
            expert_vector.append(0)
            
    # about the subject       
    if subject:
        ans = expert.ask('I will give you a subject email header for analysis:' + subject, about='subject')
        print('Subject:')
        print(ans)
        # for request in subject_requests:
        #     expert_vector.append(expert.ask(request, about='subject')[0])
    else:
        for i in range(5):
            expert_vector.append(0)
            
    # about the text
    if text:
        ans = expert.ask('I will give you a subject email header for analysis:' + text, about='text')
        print('Text:')
        print(ans)
        # for request in text_requests:
        #     expert_vector.append(expert.ask(request, about='text')[0])
    else:
        for i in range(14):
            expert_vector.append(0)
        
    aff(expert_vector)