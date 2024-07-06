import email
from email import policy
from email.parser import BytesParser
from base64 import b64decode
import quopri
import sys
from bs4 import BeautifulSoup
import html2text
import re
# import html.parser

# # Load the EML file
with open(sys.argv[1], 'rb') as eml:
    msg = BytesParser(policy=policy.default).parse(eml)

# # Print headers
# for header, value in msg.items():
#     if header == 'Content-Transfer-Encoding'
#         print(filename)
#     print(f"{header}: {value}")



# iterare mail.
html_content = html2text.HTML2Text()
html_content.ignore_links = False
# for part in msg.walk():
#     if part.get_content_type() == 'text/html':
#         # print(part.get_payload())
#         html = str(b64decode(part.get_payload()))
#         print(html)
#         text = html_content.handle(html)
#         soup = BeautifulSoup(html, 'html.parser')
        
#         for link in soup.find_all('a'):
#             print(link.get('href'))
        
for part in msg.walk():
    if part.get_content_type() == 'text/html':
        html = quopri.decodestring(part.get_payload())
        print(html)
# print("-----------------------------------------------")
# print("Links: ")
# print(urls)
    