# extract all the emails from a given .mbox file and saves them at a specified location;
# the files will be in the .eml format;

import mailbox
import os
import sys

def extract_eml_from_mbox(mbox_file, output_dir):
    # Open the mbox file
    mbox = mailbox.mbox(mbox_file)
    
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Extract each message and save as .eml file
    for index, content in enumerate(mbox):
        eml_file_path = os.path.join(output_dir, f"email_{index + 1}.eml")
        with open(eml_file_path, 'w') as eml_file:
            eml_file.write(content.as_string())
        # log progress
        print(f"Saved {eml_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 extract_eml_from_mbox [path to the .mbox file] [destination folder for .eml files]")
        exit()
    mbox_file = sys.argv[1]
    output_dir = sys.argv[2]
    extract_eml_from_mbox(mbox_file, output_dir)
