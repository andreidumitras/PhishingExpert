from email import policy                    # for reading emails
from email.parser import BytesParser        # for reading emails
# import sys                                  # for command line arguments
import os                                   # for iterating through files
import csv                                  # for constructing the dataset in .csv format
import random

import extractor                    # for extracting data from .eml file
import detective                    # for processing data extracted from .eml file
from expert import Expert           # for analysing data extracted from .eml file, with the help of LLMs


def interclass_lists(list1: list[str], list2: list[str]) -> list[list[str], bool]:
    lst = []
    i, j = 0, 0
    # split list1 in 80-20 parts for interclassing
    list1_80 = int(len(list1) * 0.8)
    list2_80 = int(len(list2) * 0.8)
    # interclassing the first 80%
    while i < list1_80 and j < list2_80:
        option = random.randrange(0, 2)
        if option == 1:
            lst.append([list1[i], 1])
            i += 1
        else:
            lst.append([list2[j], 0])
            j += 1
    while i < list1_80:
        lst.append([list1[i], 1])
        i += 1
    while j < list2_80:
        lst.append([list2[j], 0])
        j += 1
    # interclassing the last 20%
    while i < len(list1) and j < len(list2):
        option = random.randrange(0, 2)
        if option == 1:
            lst.append([list1[i], 1])
            i += 1
        else:
            lst.append([list2[j], 0])
            j += 1
    while i < len(list1):
        lst.append([list1[i], 1])
        i += 1
    while j < len(list2):
        lst.append([list2[j], 0])
        j += 1
  
    return lst

def construct_detective_vector(sender_addr: str, rr_addr: str, nr_rec: int, status_SPF: str, subj: str, text: str) -> list[float]:
    sender_localpart = None
    sender_domain = None
    if sender_addr:
        split = sender_addr.split('@')
        sender_localpart = split[0]
        sender_domain = split[1]
        
    nr_words = extractor.get_number_of_words(text)
    
    detective_vector = [
        detective.is_sender_replying_returning_to_itself(sender_addr, rr_addr),
        detective.has_sender_address_unrecomended_characters(sender_localpart),
        detective.is_domanin_common(sender_domain),
        detective.get_receivers_quotient(nr_rec),
        detective.is_SPF_passed(status_SPF),
        detective.is_empty(subj),
        detective.get_subject_length_quotient(subj),
        detective.has_odd_whitespaces(subj),
        detective.is_subject_reply(subj),
        detective.is_subject_forwarded(subj),
        detective.is_empty(text),
        detective.get_reading_time_quotient(nr_words),
        detective.has_odd_whitespaces(text)
    ]
    return detective_vector

def construct_expert_vector(sender_address: str, subject: str, text: str) -> list[float]:
    # initializing requests for each cathegory
    # sender's email address:
    sender_email_address_requests = [
        'Give me a percentage of how unusual is the email address',
        'Give me a percentage of how professional is the format of the email address',
        'Give me the probability that this email address was spoofed'
    ]
    # Subject requests (Gragg's psychological triggers)
    subject_requests = [
        'Give me the probability that this subject header is promissing something',
        'Give me the probability that this subject header is inducing a sense of urgency',
        'Give me the probability that the subject header is inducing a sense of trust for an email',
        'Give me the probability that the subject header is coming from an authoritative and credible source',
        'Give me the percentage of how suspicious is the structure of this header'
    ]
    # Text requests (Cialdini's persuasion principles)
    text_requests = [
        'Give me the probability that other people are mentioned in this text',
        'Give me the probability that this text convey a sense of urgency',
        'Give me the percentage of the authoritative tone',
        'Give me the percentage of the flattery present in the email text and how much it tries to connect with the receiver',
        'Give me the percentage of how clear is that the receiver have to do something',
        'Give me the percentage of how clear is that there is a reward or an enticing offer for the receiver',
        'Give me a percentage of how professional is the structure of the email',
        'Give me a percentage of how personalized is the email',
        'Give me a percentage of how vague is the tone and the content of the given email',
        'Give me a percentage that suggests how much the text is talking about user\'s personal information; like credit cards, passwords, accounts or a billing address',
        'Give me the percentage of how plausible is the narrative',
        'Give me the probability that the following text is containing grammatical errors',
        'Give me a percentage of how suspicious are all the links mentioned in the email',
        'Give me a percentage of how suspicious for phishing is this email overall'
    ]
    expert_vector = []
    
    # initiate the expert
    expert = Expert()
    # set the model
    expert.model = 'lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF'
    
    # ask about sender's email address
    if sender_address:
        expert.ask('Please memorize the following context:' + sender_address, quiet=True)
        for request in sender_email_address_requests:
            expert_vector.append(expert.ask(request) / 100)
    else:
        for _ in range(3):
            expert_vector.append(0)
    # ask about subject
    if subject:
        expert.ask('Please memorize the following context:' + subject, quiet=True)
        for request in subject_requests:
            expert_vector.append(expert.ask(request) / 100)
    else:
        for _ in range(5):
            expert_vector.append(0)
    # ask about the text
    if text:
        expert.ask('Please memorize the following context:' + text, quiet=True)
        for request in text_requests:
            expert_vector.append(expert.ask(request) / 100)
    else:
        for _ in range(14):
            expert_vector.append(0)
    
    return expert_vector

# main "function"
if __name__ == "__main__":
    # setting the paths for phishing and ham emails
    phish_path = '../Datasets/phishing/'
    ham_path = '../Datasets/ham/'
    
    # constructing lists with the phishing and ham emails
    phish_eml_list = [phish_path + phish_eml for phish_eml in os.listdir(phish_path)]
    ham_eml_list = [ham_path + ham_eml for ham_eml in os.listdir(ham_path)]
    
    # construct randomly interclassed list from the two lists constructed above
    emllist = interclass_lists(phish_eml_list, ham_eml_list)
    total = len(emllist)
    step = 100 / total
    percentage = step

    # prepare for .csv file
    csvheaders = [
        'return/reply address is the same with the sender address',
        'unusual characters in the sender email address',
        'sender has common email address',
        'receivers (To) quocient',
        'SPFstatus',
        'subject is empty',
        'subject length quotient',
        'subject has odd characters and whitespaces',
        'subject is replyed',
        'subject is forwarded',
        'text is empty',
        'text reading time in an hour',
        'text has odd characters and whitespaces',
        'sender address unusualness',
        'sender address professionality',
        'sender address is spoofed',
        'subject is promising',
        'subject inducing urgency',
        'subject inducing trust',
        'subject is authoritative and credible',
        'subject overall strangeness',
        'text social proof',
        'text urgency',
        'text authority',
        'text flattery and personal connection',
        'text consistancy and call to action',
        'text rewarding',
        'text professionalism',
        'text is personal',
        'text vagueness',
        'text mentions personal info',
        'text narrative plausibility',
        'text grammatical errors',
        'text has suspicious URLs',
        'text suspiciousness overall',
        'is phishing (1/0)'
    ]
    csvfile = open('./llama3.csv', mode='w', newline='')
    csv_writter = csv.writer(csvfile)
    csv_writter.writerow(csvheaders)
    
    # iterate through all of the files, extract data and construct the email vector
    for i in range(total):
        # open .eml file to read from it
        with open(emllist[i][0], 'rb') as eml:
            emlobject = BytesParser(policy = policy.default).parse(eml)
        # fill email addresses and other details
        sender_address = extractor.get_sender_address(emlobject)
        reply_return_address = extractor.get_return_address(emlobject) or extractor.get_reply_address(emlobject)
        number_of_receivers = extractor.get_number_of_receivers(emlobject)
        status_SPF = extractor.get_SPF_status(emlobject)
        # extract subject
        subject = extractor.get_subject(emlobject)
        # extract text
        text = extractor.get_text(emlobject)

        # construct the vector formed through direct and programatically observations
        detective_vector = construct_detective_vector(sender_address, reply_return_address, number_of_receivers, status_SPF, subject, text)
        # construct the vector formed with the help of LLMs
        expert_vector = construct_expert_vector(sender_address, subject, text)
        # construct the final vector: email vector
        email_vector = detective_vector + expert_vector
        email_vector.append(emllist[i][1])
        
        print(emllist[i][0], '................', percentage, '%')
        print('Email vector:', email_vector)
        percentage += step
        # write email vector to the .csv file
        csv_writter.writerow(email_vector)
    
    # close the .csv file at the end
    csvfile.close()
        