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
    sender_email_address_questions = [
        'How professional seems to be the given email address?',
        'How official and legit seems to be the given email address?',
        'How likely is to be from a personal user?'
    ]
    
    subject_questions = [
        'In what percentage does the given email Subject header induce fear?',
        'In what percentage does the given email Subject header create a sense of trust?',
        'How critical and urgent is the tone of the given email Subject header?',
        'How authoritative is the tone of the given email Subject header?',
        'How enticing and encouraging is the given email Subject header?',
        'How catchy and eye captivating is the given email Subject header?',
        'In what percentage does the given email Subject header promise or mention a reward?',
        'How neutral is the given email Subject header tone?',
        'How official seems to be the given email Subject header?'
    ]
    
    content_questions = [
        'How social proof is the given text and how much it sugests that other people were already involved in the story?',
        'How much scarcity has the given text and how much it suggests that this is a unique chance to obtain something?',
        'How authoritative is the tone of the given text?',
        'How likely is to come to an official source?',
        'How much it suggests that the user has done or said something before and now it must keep his/her promisse to the sender?',
        'How much it tryes to connect with the receiver and how likeable is trying to be?',
        'How much does it feels that the user has received something in the past from the sender?',
        'How much does the text suggests the presence of a reward or a free gift?',
        'How much does the text suggests the presence of a reward or a free gift?',
        'How professional is the tone?',
        'How personalized and tailored for the user is the given text?',
        'How vague is the tone and the content of the given text?',
        'How much is trying to spark the curiosity of the user?',
        'In what percent it seems to ask the user to take action?',
        'In what percent it seems to be a time pressure for the user to act?',
        'How detailed are the provided instructions?',
        'In what percent is the given text mentioning personal information like credit cards, passwords, accounts or a billing address?',
        'How neutral seems the tone of the given text to be?',
        'How plausible is the narrative of the given text?',
        'How coherent is the given text?',
        'Are there any grammar errors? Say 100% if there is at least one error, and 0% if there are none.',
        'Are there any grammar errors? Say 100% if there is at least one error, and 0% if there are none.',
        'How suspicious are the embedded links (if there are any)?'
    ]
    
    expert_vector = []
    
    expert = Expert()
    expert.model = 'lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF'
    # about the sender
    if sender_address:
        expert.personality = 'You are specialist in phishing detection and in recognising spoofed email address. You will provide answers in percentage followed by a short explanation of your reasoning.\nOutput: x% explanation'
        expert.ask('I will give you an email address from the From email header.', quiet=True)
        expert.ask(sender_address)
        for question in sender_email_address_questions:
            expert_vector.append(expert.ask(question)[0])
    
    # about the subject
    expert.personality = 'You are specialist in phishing detection and in recognising suspicious emails Subjects. You will provide answers in percentage followed by a short explanation of your reasoning.\nOutput: x% explanation'
    expert.ask('I will give you an email Subject header to analyze.', quiet=True)
    expert.ask(subject)
    for question in subject_questions:
        expert_vector.append(expert.ask(question)[0])
        
    aff(expert_vector)