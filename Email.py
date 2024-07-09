from email import policy
from email.parser import BytesParser
from email.header import decode_header
import lists

def frequency(text: str, charset: str) -> None:
    characters = {}
    for char in text:
        if char.encode(charset) in characters.keys():
            characters[char.encode(charset)] += 1
        else:
            characters[char.encode(charset)] = 1
    for pair in characters.items():
        print(pair)

if __name__ == "__main__":
    import sys

# email_file is a global known object
    with open(sys.argv[1], 'rb') as eml_file:
        email_file = BytesParser(policy=policy.default).parse(eml_file)
    print(sys.argv[1])
    subject = decode_header(email_file.get("Subject"))
    print(subject)
    # print(email_file.get("Subject"))
    frequency(subject[0][0], 'utf-8')
    for char in subject:
        if char in lists.unicode_whitespaces:
            print("found:", char)
            break
            
    # if email_file.is_multipart():
    #     i = 0
    #     for part in email_file.walk():
    #         # print("Content_transfer_encoding: ", part.get("Content-Transfer-Encoding"))
    #         # print(charset)
    #         # print(type(text))
    #         content_type = part.get("Content-Type")
    #         content, charset = content_type.split(';')
    #         print(content)
    #         print(charset)
    #         # charset = content_type.split(';')[1].strip().split('=')[1].strip('"')
    #         print(f"Part {i}")
    #         text = part.get_payload(decode=True)
    #         if text:
    #             # text = text.strip().decode(encoding=charset, errors="replace")
    #             # print(type(text.__str__()))
    #             # print(text.__str__())
    #             # frequency(text, charset)
    #             # print(text)
    #             pass
                
    #         i += 1
    # else:
    #     # print("Content_transfer_encoding: ", email_file.get("Content-Transfer-Encoding"))
    #     content_type = email_file.get("Content-Type")
    #     charset = content_type.split(';')[1].strip().split('=')[1].strip('"')
    #     print(f"Part {0}")
    #     text = email_file.get_payload(decode=True)
    #     if text:
    #         text = text.strip().decode(encoding=charset, errors="replace")
    #         print(text)
    #     # print(email_file.get_payload(0))
        

