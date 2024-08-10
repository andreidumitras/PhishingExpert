import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split

import sys

if __name__ == "__main__":
    csv = pd.read_csv(sys.argv[1])
    x = csv[[
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
        ]]
    y = csv['IS PHIS']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, stratify=y, random_state=8)

    svm_model = svm.SVC()
    svm_model.fit(x_train, y_train)     # x is a dataframe therefore, we use x.values
    
    print("Resulting score:", svm_model.score(x_test, y_test) * 100)
    