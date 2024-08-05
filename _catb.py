from sklearn.model_selection import train_test_split, GridSearchCV        # for splitting data into 80-20
from sklearn.metrics import mean_absolute_error
from catboost import CatBoostRegressor
import matplotlib.pyplot as plt
import pandas as pd         # for handling data
import sys                  # for command line arguments

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

    # split the data
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, stratify=y, random_state=8)
        # x - matricea de feature-uri
        # y - vectorul coloana de rezultate
        # test_size - cat % sa fie impartirea pentru test
        # stratify - pastreaza distributia claselor (doar 2, 1/0 in cazul meu) atat in test cat si in train
        # random_state - o samanta care genereaza aceleasi numere random, util ori de cate ori se ruleaza codul (va da aceleasi rezultate)
        
    # Training
    parameters = {
        "deepth": [3, 4, 5, 6],
        "learning_rate": [0.01, 0.05, 0.1],
        "n_estimators": [20, 25, 30, 40]
    }
    catb_model = GridSearchCV(CatBoostRegressor(silent=True), parameters)     # creates models with all kind of parameters
    catb_model.fit(x_train, y_train)
    
    print("Best parameters: ", catb_model.best_params_)
    
    # Evaluating
    y_pred = catb_model.predict(x_test) 
    print(f"test MAE: {round(mean_absolute_error(y_test, y_pred))}")
    
    # Best features
    feature_importance = catb_model.get_feature_importance().round(3)
    features = dict(zip(x_train.columns, feature_importance))
    print(features)
