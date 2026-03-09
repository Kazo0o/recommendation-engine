import pandas as pd
import numpy as np
from core.database import engine
from faker import Faker

fake = Faker()

def generate_data(n=1000):
    data = {
        'user_id': np.random.randint(1, 100, n),
        'item_id': np.random.randint(1, 50, n),
        'interaction_score': np.random.randint(1, 6, n),
        'timestamp': [fake.date_time_this_year() for _ in range(n)]
    }
    df = pd.DataFrame(data)
    df.to_sql('interactions', engine, if_exists='replace', index=False)
    print(f"Successfully generated and inserted {n} rows of data into the interactions table.")

if __name__ == "__main__":
    generate_data()