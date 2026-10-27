import pandas as pd


def parse_schema(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(
        pickup_datetime=pd.to_datetime(df["pickup_datetime"], errors="coerce"),
        dropoff_datetime=pd.to_datetime(df["dropoff_datetime"], errors="coerce"),
        fare_amount=df["total_amount"].astype(float),
        trip_distance=df["trip_distance"].astype(float),
    )


if __name__ == "__main__":
    df = pd.read_csv("data/yellow_tripdata_2026.csv")
    print(parse_schema(df=df))
