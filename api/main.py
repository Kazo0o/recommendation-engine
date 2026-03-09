# simple inference API using FastAPI to serve the trained model
from fastapi import FastAPI
import mlflow.sklearn
import pandas as pd
from core.database import engine

app = FastAPI()

# load the model directly from MLflow registry
model = mlflow.sklearn.load_model("models:/clustering_model/1") # type: ignore

@app.get("/recommend/{user_id}")
async def get_recommendations(user_id: int):
    # First, find the user's clusters
    user_cluster_df = pd.read_sql(f"SELECT cluster FROM user_clusters WHERRE user_id = {user_id}", engine)

    if user_cluster_df.empty:
        return {"message": "New user - showing trending items instead"}

    cluster_id = user_cluster_df.iloc[0]['cluster']

    # Rule-based Filtering (Top items in that cluster)
    recommendations = pd.read_sql(f"""
        SELECT item_id, AVG(score) as rank
        FROM interactions i
        JOIN user_clusters u ON i.user_id = u.user_id
        WHERE u.cluster = {cluster_id}
        GROUP BY item_id
        ORDER BY rank DESC
        LIMIT 10""", engine)

    return {"user_id": user_id, "cluster": int(cluster_id), "recommendations": recommendations.to_dict(orient='records')}