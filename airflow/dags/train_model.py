from airflow import DAG
from airflow.operators.python import PythonOperator # type: ignore
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import mlflow
import mlflow.sklearn
from sklearn.cluster import KMeans
from core.database import engine

def train_model():
    # connect to the db
    df = pd.read_sql("""
        SELECT user_id,
               COUNT(item_id) as total_clicks,
               AVG(score) as avg_score
        FROM interactions
        GROUP BY user_id
    """, engine)

    # start mlflow experiment
    mlflow.set_tracking_uri('http://mlflow:5000')
    mlflow.set_experiment('rec_engine_experiment')
    with mlflow.start_run():
        # simple clustering model
        n_clusters = 3
        model = KMeans(n_clusters=n_clusters, random_state=42)
        df['cluster'] = model.fit_predict(df[['total_clicks', 'avg_score']])

        # log to mlflow
        mlflow.log_param("n_clusters", n_clusters)
        mlflow.log_metric("inertia", model.inertia_)
        mlflow.sklearn.log_model(model, "clustering_model") # type: ignore

        print("Model trained and logged to MLflow")

        df.to_sql('user_clusters', engine, if_exists='replace', index=False)
with DAG(
    'ML_training_pipeline',
    start_date=datetime(2026, 1, 1),
    schedule='@hourly',
    catchup=False
) as dag:
    training_task = PythonOperator(
        task_id="train_and_log_model",
        python_callable=train_model
    )
