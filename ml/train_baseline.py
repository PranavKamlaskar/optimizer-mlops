import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, accuracy_score
import mlflow
import mlflow.sklearn
import joblib

DATA_PATH = "data/datasets/build_dataset.csv"
MODEL_DIR = "models"
EXPERIMENT_NAME = "ci_cd_failure_baseline"

os.makedirs(MODEL_DIR, exist_ok=True)

def load_data():
    df = pd.read_csv(DATA_PATH)
    # use error_text if available, otherwise cleaned_text
    df["text"] = df["error_text"].fillna("") + " " + df["cleaned_text"].fillna("")
    X = df["text"]
    y = df["status"]
    return X, y

def main():
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment(EXPERIMENT_NAME)

    X, y = load_data()
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    vectorizer = TfidfVectorizer(
        max_features=20000,
        ngram_range=(1, 2),
        min_df=2
    )

    X_train_vec = vectorizer.fit_transform(X_train)
    X_val_vec = vectorizer.transform(X_val)

    with mlflow.start_run():
        # define model
        C = 1.0
        max_iter = 200
        clf = LogisticRegression(
            C=C,
            max_iter=max_iter,
            n_jobs=-1,
            class_weight="balanced"
        )

        # log params
        mlflow.log_param("C", C)
        mlflow.log_param("max_iter", max_iter)
        mlflow.log_param("vectorizer_max_features", 20000)

        clf.fit(X_train_vec, y_train)

        # evaluate
        val_probs = clf.predict_proba(X_val_vec)[:, 1]
        val_preds = (val_probs >= 0.5).astype(int)

        auc = roc_auc_score(y_val, val_probs)
        acc = accuracy_score(y_val, val_preds)

        mlflow.log_metric("val_auc", auc)
        mlflow.log_metric("val_accuracy", acc)

        print(f"Validation AUC: {auc:.4f}")
        print(f"Validation Accuracy: {acc:.4f}")

        # save model and vectorizer locally
        model_path = os.path.join(MODEL_DIR, "baseline_logreg.pkl")
        vec_path = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
        joblib.dump(clf, model_path)
        joblib.dump(vectorizer, vec_path)

        # log to MLflow
        mlflow.sklearn.log_model(clf, "model")
        mlflow.log_artifact(vec_path, artifact_path="vectorizer")

        print("Saved model to:", model_path)
        print("Saved vectorizer to:", vec_path)

if __name__ == "__main__":
    main()

