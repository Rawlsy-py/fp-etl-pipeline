import pandas as pd

from src.transform import parse_schema


def make_input_df():
    return pd.DataFrame(
        {
            "pickup_datetime": ["2023-01-01 12:00:00", "not-a-date"],
            "dropoff_datetime": ["2023-01-01 12:30:00", "2023-01-02 12:30:00"],
            "total_amount": ["10.5", "0.0"],
            "trip_distance": ["1.25", "0.0"],
            "vendor_id": [1, 2],
        }
    )


def test_parse_schema_transforms_types_and_values():
    input_df = make_input_df()

    result_df = parse_schema(input_df)

    assert pd.api.types.is_datetime64_any_dtype(result_df["pickup_datetime"])
    assert pd.api.types.is_datetime64_any_dtype(result_df["dropoff_datetime"])
    assert pd.api.types.is_float_dtype(result_df["fare_amount"])
    assert pd.api.types.is_float_dtype(result_df["trip_distance"])
    assert result_df["pickup_datetime"].iloc[0] == pd.Timestamp("2023-01-01 12:00:00")
    assert pd.isna(result_df["pickup_datetime"].iloc[1])
    assert result_df["dropoff_datetime"].iloc[0] == pd.Timestamp("2023-01-01 12:30:00")
    assert result_df["fare_amount"].tolist() == [10.5, 0.0]
    assert result_df["trip_distance"].tolist() == [1.25, 0.0]
    assert result_df["vendor_id"].tolist() == [1, 2]


def test_parse_schema_enforces_immutability():
    input_df = make_input_df()
    original_df = input_df.copy(deep=True)

    result_df = parse_schema(input_df)

    pd.testing.assert_frame_equal(input_df, original_df)
    assert result_df is not input_df
