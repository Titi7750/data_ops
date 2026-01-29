""" Quality tests for cleaned customer data. """

import os
import pandas as pd
import numpy as np

# -----

class TestDataQuality:
    """ Class to test the quality of cleaned customer data. """

    @staticmethod
    def load_cleaned_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """ Load cleaned data from processed CSV files. """

        base_path = os.path.join(os.getcwd(), "data", "processed")

        df1 = pd.read_csv(
            os.path.join(base_path, "customers_cleaned.csv"),
            parse_dates=["signup_date"],
        )
        df2 = pd.read_csv(
            os.path.join(base_path, "customers_cleaned2.csv"),
            parse_dates=["signup_date"],
        )
        df3 = pd.read_csv(
            os.path.join(base_path, "customers_cleaned3.csv"),
            parse_dates=["signup_date"],
        )

        return df1, df2, df3

    # -----

    def test_files_exist(self) -> None:
        """ Verify that cleaned data files exist. """

        base_path = os.path.join(os.getcwd(), "data", "processed")

        assert os.path.exists(os.path.join(base_path, "customers_cleaned.csv"))
        assert os.path.exists(os.path.join(base_path, "customers_cleaned2.csv"))
        assert os.path.exists(os.path.join(base_path, "customers_cleaned3.csv"))

        return None

    # -----

    def test_dataframes_not_empty(self) -> None:
        """ Verify that the dataframes are not empty. """

        df1, df2, df3 = self.load_cleaned_data()

        assert len(df1) > 0
        assert len(df2) > 0
        assert len(df3) > 0

        return None

    # -----

    def test_required_columns_df1(self) -> None:
        """ Verify that required columns exist in df1. """

        df1, _, _ = self.load_cleaned_data()
        required_cols = ["customer_id", "full_name", "email", "signup_date", "country", "age", "last_purchase_amount", "loyalty_tier"]

        for col in required_cols:
            assert col in df1.columns

        return None

    # -----

    def test_required_columns_df2(self) -> None:
        """ Verify that required columns exist in df2. """

        _, df2, _ = self.load_cleaned_data()
        required_cols = ["customer_id", "full_name", "email", "signup_date", "country", "age", "last_purchase_amount", "loyalty_tier"]

        for col in required_cols:
            assert col in df2.columns

        return None

    # -----

    def test_required_columns_df3(self) -> None:
        """ Verify that required columns exist in df3. """

        _, _, df3 = self.load_cleaned_data()
        required_cols = ["customer_id", "full_name", "email", "signup_date", "country", "age", "last_purchase_amount", "loyalty_tier"]

        for col in required_cols:
            assert col in df3.columns

        return None

    # -----

    def test_age_valid_range(self) -> None:
        """ Verify that ages are within the valid range (16 to 99). """

        df1, df2, df3 = self.load_cleaned_data()

        for df in [df1, df2, df3]:
            assert df["age"].min() >= 16
            assert df["age"].max() <= 99

        return None

    # -----

    def test_no_null_ages(self) -> None:
        """ Verify that there are no null values in the age column. """

        df1, df2, df3 = self.load_cleaned_data()

        for df in [df1, df2, df3]:
            assert df["age"].isnull().sum() == 0

        return None

    # -----

    def test_signup_date_format(self) -> None:
        """ Verify that signup dates are in datetime format. """

        df1, df2, df3 = self.load_cleaned_data()

        for df in [df1, df2, df3]:
            assert pd.api.types.is_datetime64_any_dtype(df["signup_date"])

        return None

    # -----

    def test_no_null_dates(self) -> None:
        """ Verify that there are no null values in the signup_date column. """

        df1, df2, df3 = self.load_cleaned_data()

        for df in [df1, df2, df3]:
            assert df["signup_date"].isnull().sum() == 0

        return None

    # -----

    def test_email_format(self) -> None:
        """ Verify that all emails contain @. """

        df1, df2, df3 = self.load_cleaned_data()

        for df in [df1, df2, df3]:
            invalid_emails = df[~df["email"].str.contains("@", na=False)]
            assert len(invalid_emails) == 0

        return None

    # -----

    def test_no_duplicate_emails(self) -> None:
        """ Verify that there are no duplicate emails. """

        df1, df2, df3 = self.load_cleaned_data()

        for df in [df1, df2, df3]:
            duplicates = df["email"].duplicated().sum()
            assert duplicates == 0

        return None

    # -----

    def test_country_uppercase(self) -> None:
        """ Verify that countries are in uppercase. """

        df1, df2, df3 = self.load_cleaned_data()

        for df in [df1, df2, df3]:
            lowercase = df[df["country"].str.contains("[a-z]", na=False, regex=True)]
            assert len(lowercase) == 0

        return None

    # -----

    def test_purchase_amount_non_negative(self) -> None:
        """ Verify that all purchase amounts are non-negative. """

        df1, df2, df3 = self.load_cleaned_data()

        for df in [df1, df2, df3]:
            negative = (df["last_purchase_amount"] < 0).sum()
            assert negative == 0

        return None

    # -----

    def test_no_null_purchase_amounts(self) -> None:
        """ Verify that there are no null purchase amounts. """

        df1, df2, df3 = self.load_cleaned_data()

        for df in [df1, df2, df3]:
            nulls = df["last_purchase_amount"].isnull().sum()
            assert nulls == 0

        return None

    # -----

    def test_loyalty_tier_valid_values_df3(self) -> None:
        """ Verify that df3 does not contain UNKNOWN in loyalty_tier. """

        _, _, df3 = self.load_cleaned_data()

        unknown_count = (df3["loyalty_tier"] == "UNKNOWN").sum()
        assert unknown_count == 0

        return None

    # -----

    def test_no_null_email(self) -> None:
        """ Verify that there are no null emails. """

        df1, df2, df3 = self.load_cleaned_data()

        for df in [df1, df2, df3]:
            nulls = df["email"].isnull().sum()
            assert nulls == 0

        return None

    # -----

    def test_email_contains_domain(self) -> None:
        """ Verify that all emails contain a domain. """

        df1, df2, df3 = self.load_cleaned_data()

        for df in [df1, df2, df3]:
            invalid = df[~df["email"].str.contains(r"\w+@\w+\.\w+", na=False, regex=True)]
            assert len(invalid) == 0

        return None
