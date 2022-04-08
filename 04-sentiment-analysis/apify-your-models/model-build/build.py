""" Goal of this module:
 Build a logistic regression model in Python in order to
 determine whether candidates would get admitted to a
 prestigious university:
 
 GMAT = Graduate Management Admission Test (200-800)
 GPA = Grade Point Average (1-5)
 Work experience = Years of work experience
"""

import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


MODEL_FILENAME = "logreg.pkl"


def get_data():
    candidates = {
        'gmat': [780, 750, 690, 710, 680, 730, 690, 720, 740, 690,
                 610, 690, 710, 680, 770, 610, 580, 650, 540, 590,
                 620, 600, 550, 550, 570, 670, 660, 580, 650, 660,
                 640, 620, 660, 660, 680, 650, 670, 580, 590, 690],
        'gpa': [4, 3.9, 3.3, 3.7, 3.9, 3.7, 2.3, 3.3, 3.3, 1.7, 2.7,
                3.7, 3.7, 3.3, 3.3, 3, 2.7, 3.7, 2.7, 2.3, 3.3, 2,
                2.3, 2.7, 3, 3.3, 3.7, 2.3, 3.7, 3.3, 3, 2.7, 4,
                3.3, 3.3, 2.3, 2.7, 3.3, 1.7, 3.7],
        'work_experience': [3, 4, 3, 5, 4, 6, 1, 4, 5, 1, 3, 5, 6,
                            4, 3, 1, 4, 6, 2, 3, 2, 1, 4, 1, 2, 6,
                            4, 2, 6, 5, 1, 2, 4, 6, 5, 1, 2, 1, 4, 5],
        'admitted': [1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0,
                     0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0,
                     1, 1, 1, 0, 0, 0, 0, 1]
    }
    df = pd.DataFrame(candidates, columns=['gmat', 'gpa', 'work_experience', 'admitted'])

    return df


def build_model():
    df = get_data()
    X = df[['gmat', 'gpa', 'work_experience']]
    y = df['admitted']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=0
    )
    logistic_regression = LogisticRegression()
    logistic_regression.fit(X_train, y_train)
    y_pred = logistic_regression.predict(X_test)

    with open(MODEL_FILENAME, "wb") as f_write:
        pickle.dump(logistic_regression, f_write)

    return X_test


def load_model():
    with open(MODEL_FILENAME, "rb") as f_read:
        model: LogisticRegression = pickle.load(f_read)
        return model


def load_model_predict(x):
    model = load_model()
    return model.predict(x)


def run():
    x_test = build_model()
    predict = load_model_predict(x_test)
    print(f"predict: {predict}")


if __name__ == "__main__":
    run()
