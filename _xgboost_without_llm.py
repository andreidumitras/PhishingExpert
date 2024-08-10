import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, learning_curve       # for splitting data into 80-20
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score, RocCurveDisplay
from category_encoders.target_encoder import TargetEncoder
from xgboost import XGBClassifier
from skopt import BayesSearchCV
from skopt.space import Real, Integer
import pandas as pd         # for handling data
import numpy as np
import sys                  # for command line arguments

def search_best_model(x_train, x_test, y_train, y_test):
    encoder = TargetEncoder()
    model = XGBClassifier(random_state=8)
    
    parameters = {
        "xgb__max_depth": Integer(2, 9),
        "xgb__learning_rate": Real(0.001, 1.0, prior="log-uniform"),
        "xgb__subsample": Real(0.5, 1.0),
        "xgb__colsample_bytree": Real(0.5, 1.0),
        "xgb__colsample_bylevel": Real(0.5, 1.0),
        "xgb__colsample_bynode": Real(0.5, 1.0),
        "xgb__reg_alpha": Real(0.0, 10.0),
        "xgb__reg_lambda": Real(0.0, 10.0),
        "xgb__gamma": Real(0.0, 10.0)
    }
    pipeline = Pipeline([
        ("encoder", encoder),               # standard preprocessing procedure in classification problems (transforms in numeric values the cathegorical features)
        ("xgb", model)
    ])
    best = BayesSearchCV(
        pipeline,
        parameters,
        cv=10,
        n_iter=20,
        scoring="roc_auc",
        random_state=8,
        n_jobs=-1
    )
    best.fit(x_train, y_train)
    
    print("The best XGBoost model is with the following parameters:")
    print(best.best_params_)
    print(f"Score: {best.score(x_test, y_test)}")
    
    y_pred = best.predict(x_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.4f}")
    
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    y_prob = best.predict_proba(x_test)[:, 1]
    roc_auc = roc_auc_score(y_test, y_prob)
    print(f"ROC-AUC: {roc_auc:.4f}")
    
    RocCurveDisplay.from_estimator(best, x_test, y_test)
    plt.show()
# Learning curve
    return
    train_sizes, train_scores, test_scores = learning_curve(
        best,
        x_train,
        y_train,
        cv=5,
        scoring='accuracy',
        n_jobs=-1,
        train_sizes=np.linspace(0.1, 1.0, 10),  # 10 different training sizes
        random_state=8,
    )
    # Calculate the mean and standard deviation of the training and test scores
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    # Plot the learning curve
    plt.figure()
    plt.title("Learning Curve (XGBoost)")
    plt.xlabel("Training Examples")
    plt.ylabel("Score")

    # Plot the training and cross-validation scores
    plt.grid()
    plt.fill_between(
        train_sizes,
        train_scores_mean - train_scores_std,
        train_scores_mean + train_scores_std,
        alpha=0.1,
        color="r"
    )
    plt.fill_between(
        train_sizes,
        test_scores_mean - test_scores_std,
        test_scores_mean + test_scores_std,
        alpha=0.1,
        color="g"
    )
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r", label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g", label="Cross-validation score")

    plt.legend(loc="best")
    plt.show()
    


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
        'Attachments total-number cotient',
        'Inline total-number cotient',
        'Attachments variety',
        'Inlines variety'
        ]]
    y = csv['IS PHIS']

    # split the data
    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, stratify=y, random_state=8)
        # x - matricea de feature-uri
        # y - vectorul coloana de rezultate
        # test_size - cat % sa fie impartirea pentru test
        # stratify - pastreaza distributia claselor (doar 2, 1/0 in cazul meu) atat in test cat si in train
        # random_state - o samanta care genereaza aceleasi numere random, util ori de cate ori se ruleaza codul (va da aceleasi rezultate)
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        stratify=y,
        random_state=8
    )
    search_best_model(x_train, x_test, y_train, y_test)
