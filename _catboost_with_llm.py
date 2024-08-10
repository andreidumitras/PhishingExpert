import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score, RocCurveDisplay
from skopt import BayesSearchCV
import sys

def search_best_model(x_train, x_test, y_train, y_test):
# tunning parameters:
# Standardize the data (important for Logistic Regression)
    model = CatBoostClassifier()
    
    parameters = {
        "iterations": [100, 200, 300, 400],
        "depth": [4, 6, 8, 10],
        "learning_rate": [0.01, 0.05, 0.1, 1],
        "l2_leaf_reg": [1, 3, 5, 7, 9],
        "border_count": [32, 64, 128]
    }
        
    best = BayesSearchCV(
        model,
        parameters,
        n_iter=50,
        cv=5,
        scoring="accuracy",
        verbose=0,
        random_state=8,
        n_jobs=-1
    )
    best.fit(x_train, y_train)
    
    print("The best CatBoost model is with the following parameters:")
    print(best.best_params_)
    print(f"Score: {best.score(x_test, y_test)}")
    


def validate_best_model(x_train, x_test, y_train, y_test):
    # Build the best model:
    best = CatBoostClassifier(
        border_count=64,
        depth=8,
        iterations=300,
        l2_leaf_reg=7,
        learning_rate=0.1
    )
    best.fit(x_train, y_train)
    
# Test model's performance
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
    train_sizes, train_scores, test_scores = learning_curve(
        best,
        x_train,
        y_train,
        cv=5,
        scoring='accuracy',
        n_jobs=-1,
        train_sizes=np.linspace(0.1, 1.0, 10)  # 10 different training sizes
    )
    # Calculate the mean and standard deviation of the training and test scores
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    # Plot the learning curve
    plt.figure()
    plt.title("Learning Curve (CatBoost)")
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
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        stratify=y,
        random_state=8
    )
    search_best_model(x_train, x_test, y_train, y_test)
    # validate_best_model(x_train, x_test, y_train, y_test)