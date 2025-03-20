import os
import pandas as pd
from dotenv import load_dotenv


class BOReport:
    """
    Class to manage Biz Ops (BO) report data and operations.
    """

    def __init__(self):
        """Initialize the BOReport class by loading environment variables."""
        load_dotenv()
        self.report_path = os.getenv("BO_REPORT_PATH")
        self.data = None

    def validate_path(self):
        """Validate that the report path exists and is accessible."""
        if not self.report_path:
            raise ValueError(
                "Excel file path not found in .env file. Please set BO_REPORT_PATH."
            )

        if not os.path.exists(self.report_path):
            raise FileNotFoundError(f"Excel file not found at: {self.report_path}")

        return True

    def load_data(self):
        """
        Load data from the BO report Excel file.

        Returns:
            pandas.DataFrame: The data from the Excel file.
        """
        self.validate_path()

        try:
            self.data = pd.read_excel(self.report_path)
            print(f"Successfully read Excel file with {len(self.data)} rows.")
            return self.data
        except Exception as e:
            raise Exception(f"Error reading Excel file: {str(e)}")

    def get_data(self):
        """
        Get the loaded data or load it if not already loaded.

        Returns:
            pandas.DataFrame: The data from the Excel file.
        """
        if self.data is None:
            return self.load_data()
        return self.data


if __name__ == "__main__":
    bo_report = BOReport()
    df = bo_report.load_data()
    print(df.head())
