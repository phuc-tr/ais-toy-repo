import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import timedelta

# ---------- CONFIG ----------
CSV_PATH = "radacct10000.csv"
DB_URL = "mysql+pymysql://root:123@db/raddb"
TABLE = "radacct"
SEED = 42

INVALID_RATE = 0.05      # validity defects
NULL_RATE = 0.15         # completeness defects (>10%)
CONSISTENCY_RATE = 0.05  # timestamp inconsistency
STALE_HOURS = 48         # freshness violation (>25h)

# ---------- SETUP ----------
np.random.seed(SEED)

# ---------- LOAD BASE SNAPSHOT ----------
df = pd.read_csv(
    CSV_PATH,
    parse_dates=[
        "acctstarttime",
        "acctupdatetime",
        "acctstoptime"
    ],
)

latest_ts = df["acctstarttime"].max()
print(f"Latest timestamp in CSV (acctstarttime): {latest_ts}")
# Latest timestamp in CSV (acctstarttime): 2020-08-17 00:30:00

df = df.replace({float("nan"): None})
df["acctinterval"] = df["acctinterval"].replace("\\N", 0)

df = df.copy()
n = len(df)

# ---------- VALIDITY DEFECTS ----------
df.loc[df.sample(frac=INVALID_RATE, random_state=SEED).index, "nasportid"] = "BADFORMAT"
df.loc[df.sample(frac=INVALID_RATE, random_state=SEED + 1).index, "nasporttype"] = "Ethernet"
df.loc[df.sample(frac=INVALID_RATE, random_state=SEED + 2).index, "acctterminatecause"] = "Unknown-Cause"

# ---------- CONSISTENCY DEFECT ----------
idx = df.sample(frac=CONSISTENCY_RATE, random_state=SEED + 3).index
df.loc[idx, "acctstoptime"] = df.loc[idx, "acctstarttime"] - timedelta(minutes=5)

# ---------- ACCURACY DEFECT ----------
p90 = df["acctsessiontime"].quantile(0.90)
df.loc[df["acctsessiontime"] >= p90, "acctsessiontime"] = 60000

# ---------- COMPLETENESS DEFECTS ----------
df.loc[df.sample(frac=NULL_RATE, random_state=SEED + 4).index, "calledstationid"] = None
df.loc[df.sample(frac=NULL_RATE, random_state=SEED + 5).index, "callingstationid"] = None

# ---------- FRESHNESS DEFECT ----------
df["acctstarttime"] = df["acctstarttime"] - timedelta(hours=STALE_HOURS)
df["acctupdatetime"] = df["acctupdatetime"] - timedelta(hours=STALE_HOURS)
df["acctstoptime"] = df["acctstoptime"] - timedelta(hours=STALE_HOURS)
# ---------- LOAD INTO DB ----------
engine = create_engine(DB_URL)

df.to_sql(
    TABLE,
    con=engine,
    if_exists="append",
    index=False,
    chunksize=10,
    method="multi",
)

print(f"Inserted {len(df)} defect-injected rows into `{TABLE}`")
