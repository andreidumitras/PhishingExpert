from sklearn.model_selection import train_test_split        # for splitting data into 80-20
from sklearn.pipeline import Pipeline
from category_encoders.target_encoder import TargetEncoder
from xgboost import XGBClassifier
from xgboost import plot_importance
from skopt import BayesSearchCV
from skopt.space import Real, Integer
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
        # 'if sender impersonates something',
        # 'from suspiciopus level',
        # 'if reply address impersonates something',
        # 'reply address suspiciopus level',
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
        # 'Subject Authority',
        # 'Subject Urgency',
        # 'Subject Scarcity',
        # 'Subject Social Proof',
        # 'Subject Liking',
        # 'Subject Reciprocity',
        # 'Subject Consistancy',
        # 'Subject Punctuation',
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
        # 'Text Authority',
        # 'Text Urgency',
        # 'Text Scarcity',
        # 'Text Social Proof',
        # 'Text Liking',
        # 'Text Reciprocity',
        # 'Text Consistancy',
        # 'Text Punctuation',
        # 'Text Grammar',
        # 'Text Sensitive Information',
        'Attachments total-number cotient',
        'Inline total-number cotient',
        'Attachments variety',
        'Inlines variety'
        ]]
    y = csv['IS PHIS']

    # split the data
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, stratify=y, random_state=8)
        # x - matricea de feature-uri
        # y - vectorul coloana de rezultate
        # test_size - cat % sa fie impartirea pentru test
        # stratify - pastreaza distributia claselor (doar 2, 1/0 in cazul meu) atat in test cat si in train
        # random_state - o samanta care genereaza aceleasi numere random, util ori de cate ori se ruleaza codul (va da aceleasi rezultate)
        
    # pipeline for training
    estimators = [
        ("encoder", TargetEncoder()),               # standard preprocessing procedure in classification problems (transforms in numeric values the cathegorical features)
        ("clf", XGBClassifier(random_state=8))      # 8 because predictibility, and clf + XGBClassifier is the scikit learn implementation of XGBoost
    ]
    pipeline = Pipeline(steps=estimators)
    # this pipeline will ensure that the data is always encoded before feed into the XGBoost classifier
    
    # Set up the hyperparameters
    # use the package scikit-optimize that will perform Bayesian Optimization
    search_space = {
        "clf__max_depth": Integer(2, 8),
        "clf__learning_rate": Real(0.001, 1.0, prior="log-uniform"),
        "clf__subsample": Real(0.5, 1.0),
        "clf__colsample_bytree": Real(0.5, 1.0),
        "clf__colsample_bylevel": Real(0.5, 1.0),
        "clf__colsample_bynode": Real(0.5, 1.0),
        "clf__reg_alpha": Real(0.0, 10.0),
        "clf__reg_lambda": Real(0.0, 10.0),
        "clf__gamma": Real(0.0, 10.0)
    }
    optimisation = BayesSearchCV(pipeline, search_space, cv=10, n_iter=20, scoring="roc_auc", random_state=8)
        # cv - 5-fold cross validation
        # n_iter - 10 for starting, then increase ot 20, 50
        # scoring - the evaluation method (area under the curve and co)
    
    # Train XGBoost model
    xgb_model = optimisation.fit(x_train, y_train)
    print("Model: ",xgb_model)
    
    # Evaluate the model
    best_estimator = optimisation.best_estimator_
    print("Best estimator: ",best_estimator)
    best_score = optimisation.best_score_
    print("Training Best score:", best_score)
    print("Testing Best score:", optimisation.score(x_test, y_test))
    
    y_pred = optimisation.predict(x_test)
    print(y_pred)
    print(optimisation.predict_proba(x_test))
    
    xgb_step = optimisation.best_estimator_.steps[1]
    xgb_best_model = xgb_step[1]
    plot_importance(xgb_best_model)
