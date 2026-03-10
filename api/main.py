# main.py
from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from core.database import engine

app = FastAPI(title="NeuroVerse Recommender API")

@app.get("/recommend/{user_id}")
def get_recommendation(user_id: int):
    with engine.connect() as conn:
        # 1. Look up the user's cluster assigned by Airflow
        result = conn.execute(
            text("SELECT cluster FROM user_clusters WHERE user_id = :u"),
            {"u": user_id}
        ).fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="User profile not built yet")

        user_cluster = result[0]

        # 2. Fetch popular items from the same cluster (Collaborative Filtering logic)
        # For now, let's just grab the top-rated items in that cluster
        recommendations = conn.execute(
            text("""
                SELECT item_id, AVG(interaction_score) as score
                FROM interactions
                JOIN user_clusters ON interactions.user_id = user_clusters.user_id
                WHERE user_clusters.cluster = :c
                GROUP BY item_id
                ORDER BY score DESC
                LIMIT 5
            """),
            {"c": user_cluster}
        ).fetchall()

    return {
        "user_id": user_id,
        "cluster": user_cluster,
        "recommendations": [row[0] for row in recommendations]
    }