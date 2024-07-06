# main module
import feature_parser
# import detective
# import expert
# import urls_specialist
# import classifier
 
from email import policy
from email.parser import BytesParser
import sys

# email_file is a global known object
with open(sys.argv[1], 'rb') as eml_file:
    email_file = BytesParser(policy=policy.default).parse(eml_file)
feature_parser.get_sender_address()
    
