""" Tests for clean_customers_data function. """

import pandas as pd
from src.clean_data import clean_customers_data

# -----

class TestCleanCustomersData:
    """ Tests for the main clean_customers_data function. """

    def test_clean_customers_data_basic(self) -> None:
        """ Test basic cleaning of three dataframes. """

        df1 = pd.DataFrame({
            "age": [25, 30],
            "signup_date": ["2024-01-15", "2024-02-20"],
            "email": ["user1example.com", "user2@example.com"],
            "country": ["france", "usa"],
            "last_purchase_amount": [50.0, 100.0]
        })
        df2 = pd.DataFrame({
            "age": [28, 35],
            "signup_date": ["2024-03-10", "2024-04-05"],
            "email": ["john.doeexample.com", "jane.smithexample.com"],
            "full_name": ["John Doe", "Jane Smith"],
            "country": ["France", "Germany"],
            "last_purchase_amount": [75.0, 120.0]
        })
        df3 = pd.DataFrame({
            "age": [22, 45],
            "signup_date": ["2024-05-12", "2024-06-08"],
            "email": ["bob@example", "alice@domain"],
            "full_name": ["Bob Johnson", "Alice Brown"],
            "country": ["USA", "FRA"],
            "last_purchase_amount": [60.0, 90.0],
            "loyalty_tier": ["BRONZE", "UNKNOWN"]
        })

        result1, result2, result3 = clean_customers_data(df1, df2, df3)

        assert isinstance(result1, pd.DataFrame)
        assert isinstance(result2, pd.DataFrame)
        assert isinstance(result3, pd.DataFrame)

        assert "age" in result1.columns
        assert "email" in result2.columns
        assert "loyalty_tier" in result3.columns

        return None

    # -----

    def test_clean_customers_data_preserves_data(self) -> None:
        """ Test that cleaning preserves non-corrupted data. """

        df1 = pd.DataFrame({
            "age": [30],
            "signup_date": ["2024-01-15"],
            "email": ["valid@example.com"],
            "country": ["france"],
            "last_purchase_amount": [100.0]
        })
        df2 = pd.DataFrame({
            "age": [35],
            "signup_date": ["2024-03-10"],
            "email": ["jane.smith@example.com"],
            "full_name": ["Jane Smith"],
            "country": ["Germany"],
            "last_purchase_amount": [150.0]
        })
        df3 = pd.DataFrame({
            "age": [25],
            "signup_date": ["2024-05-12"],
            "email": ["bob@example.com"],
            "full_name": ["Bob Johnson"],
            "country": ["USA"],
            "last_purchase_amount": [80.0],
            "loyalty_tier": ["GOLD"]
        })

        result1, result2, result3 = clean_customers_data(df1, df2, df3)

        assert result1["age"][0] == 30
        assert result2["age"][0] == 35
        assert result3["age"][0] == 25

        return None
