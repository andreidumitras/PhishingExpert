from email import policy                    # for reading emails
from email.parser import BytesParser        # for reading emails
from bs4 import BeautifulSoup
import csv
import sys
import os
import random
import extractor
import detective
import expert

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

def zeros(n: int) -> list:
    array = []
    for i in range(n):
        array.append(0)
    return array

def envelope_analysis(emlobject, llm) -> list:
    # fill variables with data
    # From:
    # displayed name
    # sender's email address
    from_header = emlobject.get("From")
    data = extractor.get_email_address_and_displayed_name_data(from_header)
    sender_dispalyed_name = data[0]
    sender_email_address = data[1]
    # Return-Path:
    # return email address
    return_path_header = emlobject.get("Return-Path")
    data = extractor.get_email_address_and_displayed_name_data(return_path_header)
    return_email_address = data[1]
    # Reply-To:
    # displayed name
    # reply email address    
    reply_to_header = emlobject.get("Reply-To")
    data = extractor.get_email_address_and_displayed_name_data(reply_to_header)
    reply_dispalyed_name = data[0]
    reply_email_address = data[1]
    # To:
    # list of receivers
    receivers = emlobject.get("To")
    # Cc:
    # list of CCs    
    cc = emlobject.get("Cc")
    # SPF status:
    spf_status = emlobject.get("Received-SPF")
    
    correspondant_address = reply_email_address or return_email_address
    
    questions = [
        "Does it pretend to impersonate an official email address that could be from a trusted figure or organization? Give only the best probability approximation in percentage.",
        "Does it seems to be a suspicious email address? Give only the best probability approximation in percentage."
    ]
    #construct envelope features
    values = []
    values.append(detective.has_sender_email_address(sender_email_address))
    values.append(detective.has_sender_displayed_name(sender_dispalyed_name))
    values.append(detective.has_reply_email_address(reply_email_address))
    values.append(detective.has_reply_displayed_name(reply_dispalyed_name))
    values.append(detective.has_return_email_address(return_email_address))
    values.append(detective.has_same_email_address(sender_email_address, correspondant_address))
    values.append(detective.has_displayname_as_email_localpart(sender_dispalyed_name, sender_email_address))
    values.append(detective.has_displayname_as_email_localpart(reply_dispalyed_name, reply_email_address))
    values.append(detective.has_common_email_domain(sender_email_address))
    values.append(detective.has_common_email_domain(correspondant_address))
    
    if not sender_email_address:
        analysis = [0, 0]
    else:
        analysis = expert.ask_about(sender_email_address.full, llm, questions, "email address")
    values += analysis
    if not reply_email_address:
        analysis = [0, 0]
    else:
        analysis = expert.ask_about(reply_email_address.full, llm, questions, "email address")
    values += analysis
    
    values.append(detective.get_full_length(from_header))
    values.append(detective.get_displayed_name_length(sender_dispalyed_name))
    values.append(detective.get_email_address_length(sender_email_address))
    values.append(detective.get_email_address_local_part_length(sender_email_address))
    values.append(detective.get_email_address_domain_name_length(sender_email_address))
    
    values.append(detective.get_full_length(reply_to_header or return_path_header))
    values.append(detective.get_displayed_name_length(reply_dispalyed_name))
    values.append(detective.get_email_address_length(reply_email_address or return_email_address))
    values.append(detective.get_email_address_local_part_length(reply_email_address or return_email_address))
    values.append(detective.get_email_address_domain_name_length(reply_email_address or return_email_address))
    
    values.append(detective.get_amount(receivers))
    values.append(detective.get_amount(cc))
    values.append(detective.pass_spf(spf_status))
    
    return values

def subject_analysis(emlobject, llm) -> list:
    subject = emlobject.get("Subject")
    values = [
        detective.is_blank(subject),
        detective.has_unusual_characters(subject),
        detective.get_number_of_words(subject),
        detective.get_full_length(subject),
        detective.get_number_of_digits(subject),
        detective.get_number_of_caps(subject),
        detective.get_number_of_lows(subject),
        detective.what_is_subject(subject, isit="re:"),
        detective.what_is_subject(subject, isit="fwd:")
    ]
    questions = [
        "Does it pretend to come from a trusted figure, organization or company, such as a bank, government agency or company executive? Give only the best probability approximation in percentage.",
        "Does it create a sense of urgency and emphasize negative consequences if the recipient does not act quickly? Give only the best probability approximation in percentage.",
        "Does it promise a reward or exclusive offer that is only available for a short period of time? Give only the best probability approximation in percentages",
        "Does it sound like a testimonial or endorsement from a trusted individual or entity that is popular? Give only the best probability approximation in percentage.",
        "Does it sound to be personal or have a friendly tone adopting a casual attitude to create a sense of familiarity and trust? Give only the best probability approximation in percentage.",
        "Does it offer assistance or benefits such as a free discount to encourage a reciprocal action? Give Give only the best probability approximation in percentage", 
        "Does it seems to ask for a small and harmless action to increase the trust and likelihood of compliance with a larger request later? Give only the best probability approximation in percentage.",
        "Does it seem to have an odd punctuation, abusing spaces and symbols like “,.<>/?\|{}[]()-=:;!~*@#$%&” in an abnormal way or using special Unicode characters? Give only the best probability approximation in percentage."
    ]
    analysis = expert.ask_about(subject, llm, questions, "email subject")
    values += analysis
    
    return values

def body_analysis(emlobject, llm) -> list:
    # TODO:
    # extract text_payload
    values = []
    result = extractor.get_email_payloads(emlobject)
    text_payload = result[0]
    is_html = result[1]
    inlines = result[2]
    attachments = result[3]
    
    if is_html:
        soup = BeautifulSoup(text_payload, 'html.parser')
        text = extractor.get_html_text_content(soup)
        hyperlinks = extractor.get_html_hyperlinks(soup)
        
        values = [
            detective.is_blank(text),
            detective.is_text_html(is_html),
            detective.get_html_number_of_headings(soup),
            detective.get_html_number_of_paragraphs(soup),
            detective.get_html_number_of_links(hyperlinks),
            detective.get_html_number_of_distinct_links(hyperlinks),
            detective.get_html_number_of_mailto(hyperlinks),
            detective.get_html_number_of_http(hyperlinks),
            detective.get_html_number_of_images(soup),
            detective.get_html_number_of_buttons(soup),
            detective.get_html_number_of_scripts(soup),
            detective.get_number_of_words(text),
            detective.get_number_of_characters(text),
            detective.has_unusual_characters(text)
        ]
    else:
        text = extractor.get_plain_text_content(text_payload)
        hyperlinks = extractor.get_plain_hyperlinks(text)
        values = [
            detective.is_blank(text),
            0,
            0,
            detective.get_plain_number_of_paragraphs(text),
            detective.get_plain_number_of_links(hyperlinks),
            detective.get_plain_number_of_distinct_links(hyperlinks),
            detective.get_plain_number_of_mailto(hyperlinks),
            detective.get_plain_number_of_http(hyperlinks),
            0,
            0,
            0,
            detective.get_number_of_words(text),
            detective.get_number_of_characters(text),
            detective.has_unusual_characters(text)
        ]
        
    questions = [
        "Does it pretend to come from a trusted figure, organization or company, such as a bank, government agency or company executive? Give only the best probability approximation in percentage.",
        "Does it create a sense of urgency and emphasize negative consequences if the recipient does not act quickly? Give only the best probability approximation in percentage.",
        "Does it promise a reward or exclusive offer that is only available for a short period of time? Give only the best probability approximation in percentage.",
        "Does it sound like a testimonial or endorsement from a trusted individual or entity that is popular? Give only the best probability approximation in percentage.",
        "Does it sound to be personal or have a friendly tone adopting a casual attitude to create a sense of familiarity and trust? Give only the best probability approximation in percentage.",
        "Does it offer assistance or benefits such a s a free discount to encourage a reciprocal action? Give only the best probability approximation in percentage.",
        "Does it seems to ask for a small and harmless action to increase the trust and likelihood of compliance with a larger request later? Give Give only the best probability approximation in percentage", 
        "Does it seem to have an odd punctuation, abusing spaces and symbols like “,.<>/?\|{}[]()-=:;!~*@#$%&” in an abnormal way or using special Unicode characters? Give only the best probability approximation in percentage.",
        "Does it have any grammatical error and phrase inconsistency? Give only the best probability approximation in percentage.",
        "Does it seem to mention or ask for any sensitive information like card number, password, account ID, money and other personal and financial information? Give only the best probability approximation in percentage."
    ]
    analysis = expert.ask_about(text, llm, questions, "email text")
    values += analysis
    
    values.append(detective.get_number_of_attachments(attachments))
    values.append(detective.get_number_of_inlines(inlines))
    values.append(detective.get_variety(attachments))
    values.append(detective.get_variety(inlines))
    return values

def read_email(filename: str) -> str:
    with open(filename, 'rb') as emlhandle:
        emlobject = BytesParser(policy = policy.default).parse(emlhandle)
    return emlobject


if __name__ == "__main__":
    phish_path = '../Datasets/phishing/'
    ham_path = '../Datasets/ham/'
    
    # constructing lists with the phishing and ham emails
    phish_eml_list = [phish_path + phish_file for phish_file in os.listdir(phish_path)]
    ham_eml_list = [ham_path + ham_file for ham_file in os.listdir(ham_path)]
    
    # construct randomly interclassed list from the two lists constructed above
    emllist = interclass_lists(phish_eml_list, ham_eml_list)
    total = len(emllist)
    step = 100 / total
    percentage = step

    csvheaders = [
        'has from address',
        'has from displayed name',
        'has reply address',
        'has reply displayed name',
        'has return address',
        'from and correspondant address similarity',
        'displayed name and local part similarity of form',
        'displayed name and local part similarity of reply',
        'from has common email provider',
        'correspondant address has common email provider',
        'if sender impersonates something',
        'from suspiciopus level',
        'if reply address impersonates something',
        'reply address suspiciopus level',
        'from full length cotinet',
        'from displayed name length cotinet',
        'from address length cotinet',
        'from local-part length cotinet',
        'from domain length cotinet',
        'correspondant full length cotinet',
        'correspondant displayed name length cotinet',
        'correspondant address length cotinet',
        'correspondant local-part length cotinet',
        'correspondant domain length cotinet',
        'number of receivers (To) cotient',
        'number of CCs cotient',
        'PASS SPF',
        'Subject is empty',
        'Subject has unusual characters',
        'Subject number of words cotient',
        'Subject length cotient',
        'Subject number of digits cotient',
        'Subject number of caps cotient',
        'Subject number of lows cotient',
        'Subject is Fwd',
        'Subject is Re',
        'Subject Authority',
        'Subject Urgency',
        'Subject Scarcity',
        'Subject Social Proof',
        'Subject Liking',
        'Subject Reciprocity',
        'Subject Consistancy',
        'Subject Punctuation',
        'Text is blank',
        'Text has HTML',
        'Text number of headings cotient',
        'Text number of paragraphs cotient',
        'Text number of URLs cotient',
        'Text number of distict URLs cotient',
        'Text number of mailto URLs cotient',
        'Text number of http(s?) URLs cotient',
        'Text number of images cotient',
        'Text number of buttons cotient',
        'Text number of scripts cotient',
        'Text number of words cotient',
        'Text number of characters cotient',
        'Text has unusual characters',
        'Text Authority',
        'Text Urgency',
        'Text Scarcity',
        'Text Social Proof',
        'Text Liking',
        'Text Reciprocity',
        'Text Consistancy',
        'Text Punctuation',
        'Text Grammar',
        'Text Sensitive Information',
        'Attachments total-number cotient',
        'Inline total-number cotient',
        'Attachments variety',
        'Inlines variety',
        'IS PHIS'
    ]
    csvfile = open('./phi3.1.csv', mode='w', newline='')
    csv_writter = csv.writer(csvfile)
    csv_writter.writerow(csvheaders)
    
    llm = expert.Expert("lmstudio-community/Phi-3.1-mini-4k-instruct-GGUF")
    for i in range(total):
        emlobject = read_email(emllist[i][0])    
        email_vector = []
        results = envelope_analysis(emlobject, llm)
        email_vector += results
        results = subject_analysis(emlobject, llm)
        email_vector += results
        results = body_analysis(emlobject, llm)
        email_vector += results
        email_vector.append(emllist[i][1])
        print(emllist[i][0], '------------------- ', percentage, '%')
        percentage += step
        # write email vector to the .csv file
        csv_writter.writerow(email_vector)
    
    csvfile.close()
    # email_vector.append(status)