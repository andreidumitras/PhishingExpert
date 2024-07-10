import extractor
import sys
from email import policy
from email.parser import BytesParser
import os

if __name__ == '__main__':
    path = '../Datasets/phishing/'
    if len(sys.argv) > 2:
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
        
        match sys.argv[2]:
            case 'text':
                print(text)
            case 'subject':
                print(subject)
            case 'sender':
                print(sender_address)
        exit()
    for eml in os.listdir(path):
        with open(path + eml, 'rb') as eml_file:
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
        
        match sys.argv[1]:
            case 'text':
                print(text)
            case 'subject':
                print(subject)
            case 'sender':
                print(sender_address)
        