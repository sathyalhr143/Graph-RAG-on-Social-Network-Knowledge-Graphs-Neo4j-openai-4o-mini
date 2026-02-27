import pandas as pd
from pathlib import Path

# Config
USERS_URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/GSNJkoEM3yeeCjJl1l2Jrg/users.csv"
EDGES_URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/m9iBI6GCId0XoGEkjwHk3g/edges-follow.csv"

CUR = Path("data/curated"); CUR.mkdir(parents=True, exist_ok=True)
USERS_CSV = CUR / "users.csv"
EDGES_CSV = CUR / "edges_follow.csv"

# download only if missing
if not USERS_CSV.exists():
    pd.read_csv(USERS_URL).to_csv(USERS_CSV, index=False)
if not EDGES_CSV.exists():
    pd.read_csv(EDGES_URL).to_csv(EDGES_CSV, index=False)

df_users = pd.read_csv(USERS_CSV)
df_edges = pd.read_csv(EDGES_CSV)
print(df_users.head(3))
print(df_edges.head(3))
print(f"✅ users={len(df_users):,} | edges={len(df_edges):,}")