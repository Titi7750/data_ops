""" Module to clean and normalize customer data across multiple dataframes. """

import os
import pycountry
import pandas as pd

# -----

def _fix_age(param_dataframe: pd.DataFrame, param_invalid_values: list = None) -> pd.DataFrame:
    """ Fix age column: replace invalid values and convert to int. """

    if param_invalid_values:
        for value in param_invalid_values:
            param_dataframe["age"] = param_dataframe["age"].replace(value, pd.NA)

    param_dataframe["age"] = param_dataframe["age"].fillna(0).astype(int)
    param_dataframe["age"] = param_dataframe["age"].apply(lambda age: age if 16 <= age <= 99 else 16)

    return param_dataframe

# -----

def _fix_signup_date(param_dataframe: pd.DataFrame, param_replacements: dict = None) -> pd.DataFrame:
    """ Fix signup_date column: apply specific replacements and convert to datetime. """

    if param_replacements:
        for old, new in param_replacements.items():
            param_dataframe["signup_date"] = param_dataframe["signup_date"].replace(old, new)
    else:
        param_dataframe["signup_date"] = param_dataframe["signup_date"].replace("not_a_date", pd.NaT)

    param_dataframe["signup_date"] = param_dataframe["signup_date"].astype("datetime64[ns]")

    median_date = param_dataframe["signup_date"].median()
    param_dataframe["signup_date"] = param_dataframe["signup_date"].fillna(median_date)

    return param_dataframe

# -----

def _fix_email(param_dataframe: pd.DataFrame, param_specific_fix: str = None) -> pd.DataFrame:
    """ Fix email column: add missing @ signs. """

    if param_specific_fix == "format_name":
        # Dataframe 2 specific: format with first.last@domain
        param_dataframe["email"] = param_dataframe["email"].apply(
            lambda check: check if "@" in check else check.replace("example.com", "@example.com")
        )

        prenom = param_dataframe["full_name"].str.split().str[0]
        nom = param_dataframe["full_name"].str.split().str[1]
        domain = param_dataframe["email"].str.split("@").str[1]

        mask_email = param_dataframe["email"].str.contains(r"\.[a-zA-Z]@")
        param_dataframe.loc[mask_email, "email"] = (
            prenom[mask_email].str.lower()
            + "."
            + nom[mask_email].str.lower()
            + "@"
            + domain
        )

        param_dataframe.drop(columns=["prenom", "nom"] if "prenom" in param_dataframe.columns else [], inplace=True)

    elif param_specific_fix == "missing_domain":
        # Dataframe 3 specific
        param_dataframe["email"] = param_dataframe["email"].apply(
            lambda check: check if ".com" in check else check.replace("@example", "@example.com")
        )

    else:
        # Dataframe 1 default
        param_dataframe["email"] = param_dataframe["email"].apply(
            lambda check: check if "@" in check else check.replace("example.com", "@example.com")
        )

    return param_dataframe

# -----

def _fix_country(param_dataframe: pd.DataFrame, param_specific_mappings: dict = None) -> pd.DataFrame:
    """ Fix country column: standardize format and validate country codes. """

    valid_country_codes = {country.alpha_2 for country in pycountry.countries}

    if param_specific_mappings:
        for old, new in param_specific_mappings.items():
            if new.upper() not in valid_country_codes:
                raise ValueError(f"Invalid country code in mapping: '{new}'.")

            param_dataframe["country"] = param_dataframe["country"].replace(old, new)

    param_dataframe["country"] = param_dataframe["country"].str.upper()

    return param_dataframe

# -----

def _fix_purchase_amount(param_dataframe: pd.DataFrame) -> pd.DataFrame:
    """ Ensure purchase amounts are non-negative. """

    param_dataframe["last_purchase_amount"] = param_dataframe["last_purchase_amount"].astype(float)
    param_dataframe["last_purchase_amount"] = param_dataframe["last_purchase_amount"].apply(
        lambda price: price if price >= 0.0 else 0.0
    )

    return param_dataframe

# -----

def _drop_duplicate_emails(param_dataframe: pd.DataFrame) -> pd.DataFrame:
    """ Drop duplicate email entries, keeping the first occurrence. """

    param_dataframe.drop_duplicates(subset=["email"], keep="first", inplace=True)

    return param_dataframe

# -----

def clean_customers_data(param_dataframe1: pd.DataFrame, param_dataframe2: pd.DataFrame, param_dataframe3: pd.DataFrame) -> tuple:
    """
    Clean and normalize customer data across three dataframes.
    Performs operations including:
    - Type corrections (age, signup_date)
    - Email address fixes
    - Date median filling
    - Country name standardization
    - Age validation
    - Purchase amount validation
    - Loyalty tier corrections

    Args:
        df1: First customers dataframe
        df2: Second customers dataframe
        df3: Third customers dataframe

    Returns:
        tuple: Three cleaned dataframes with deletion counts
    """

    # Store original row counts
    original_count1 = len(param_dataframe1)
    original_count2 = len(param_dataframe2)
    original_count3 = len(param_dataframe3)

    # Clean Dataframe 1
    df1 = param_dataframe1.copy()
    df1 = _fix_age(df1)
    df1 = _fix_signup_date(df1)
    df1 = _fix_email(df1)
    df1 = _fix_country(df1)
    df1 = _fix_purchase_amount(df1)
    df1 = _drop_duplicate_emails(df1)

    # Clean Dataframe 2
    df2 = param_dataframe2.copy()
    df2 = _fix_age(df2)
    df2 = _fix_signup_date(df2, {"invalid_date": pd.NaT, "2025-02-29": "2025-02-28"})
    df2 = _fix_email(df2, param_specific_fix="format_name")
    df2 = _fix_country(df2, {"France": "FR"})
    df2 = _fix_purchase_amount(df2)
    df2 = _drop_duplicate_emails(df2)

    # Clean Dataframe 3
    df3 = param_dataframe3.copy()
    df3 = _fix_age(df3, param_invalid_values=["abc"])
    df3 = _fix_signup_date(df3, {
        "not_a_date": pd.NaT,
        "2025-13-01": "2025-12-01",
        "2024-02-29": "2024-02-28",
        "2025-02-30": "2025-02-28"
    })
    df3 = _fix_email(df3, param_specific_fix="missing_domain")
    df3["prenom"] = df3["full_name"].str.split().str[0]
    df3["nom"] = df3["full_name"].str.split().str[1]
    df3.dropna(subset=["prenom", "nom"] if "prenom" in df3.columns else [], inplace=True)
    df3.drop(columns=["prenom", "nom"] if "prenom" in df3.columns else [], inplace=True)
    df3 = _fix_country(df3, {"France": "FR", "FRA": "FR", "USA": "US"})
    df3 = _fix_purchase_amount(df3)
    df3["loyalty_tier"] = df3["loyalty_tier"].replace("UNKNOWN", "BRONZE")
    df3 = _drop_duplicate_emails(df3)

    # Store deletion counts in dataframe attributes
    df1.attrs["rows_deleted"] = original_count1 - len(df1)
    df2.attrs["rows_deleted"] = original_count2 - len(df2)
    df3.attrs["rows_deleted"] = original_count3 - len(df3)

    return df1, df2, df3

# -----

def save_cleaned_data(param_dataframe1: pd.DataFrame, param_dataframe2: pd.DataFrame, param_dataframe3: pd.DataFrame) -> None:
    """
    Save cleaned customer dataframes to processed CSV files.
    Displays the number of rows deleted during cleaning for each file.

    Args:
        param_dataframe1: First cleaned customers dataframe
        param_dataframe2: Second cleaned customers dataframe
        param_dataframe3: Third cleaned customers dataframe
    """

    param_dataframe1.to_csv(
        os.path.join(
            os.getcwd(),
            "data",
            "processed",
            "customers_cleaned.csv"
        ),
        index=False
    )
    rows_deleted_1 = param_dataframe1.attrs.get("rows_deleted", 0)
    print(f"Fichier 1: {rows_deleted_1} ligne(s) supprimée(s)")

    param_dataframe2.to_csv(
        os.path.join(
            os.getcwd(),
            "data",
            "processed",
            "customers_cleaned2.csv"
        ),
        index=False
    )
    rows_deleted_2 = param_dataframe2.attrs.get("rows_deleted", 0)
    print(f"Fichier 2: {rows_deleted_2} ligne(s) supprimée(s)")

    param_dataframe3.to_csv(
        os.path.join(
            os.getcwd(),
            "data",
            "processed",
            "customers_cleaned3.csv"
        ),
        index=False
    )
    rows_deleted_3 = param_dataframe3.attrs.get("rows_deleted", 0)
    print(f"Fichier 3: {rows_deleted_3} ligne(s) supprimée(s)")

    return None
