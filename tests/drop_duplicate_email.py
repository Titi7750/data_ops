""" Tests for the _drop_duplicate_emails function in clean_data.py. """

import pandas as pd
from src.clean_data import _drop_duplicate_emails

# -----

class TestDropDuplicateEmails:
    """ Tests for the _drop_duplicate_emails function. """

    def test_drop_duplicate_emails(self) -> None:
        """ Test removing duplicate emails. """

        dataframe = pd.DataFrame({
            "email": ["user1@example.com", "user2@example.com", "user1@example.com"],
            "name": ["User 1", "User 2", "User 1 Duplicate"]
        })
        result = _drop_duplicate_emails(dataframe)

        assert len(result) == 2
        assert result["email"].tolist() == ["user1@example.com", "user2@example.com"]

        return None

    # -----

    def test_drop_duplicate_emails_keeps_first(self) -> None:
        """ Test that the first occurrence is kept. """

        dataframe = pd.DataFrame({
            "email": ["admin@test.com", "admin@test.com"],
            "name": ["Admin First", "Admin Second"]
        })
        result = _drop_duplicate_emails(dataframe)

        assert len(result) == 1
        assert result["name"].iloc[0] == "Admin First"

        return None
