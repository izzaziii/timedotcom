import sys
import argparse
from typing import Optional, Dict, Any, List
import pandas as pd

from timedotcom.datasets.boreport import BOReport
from timedotcom.database.client import MongoDBClient


def get_boreport_data() -> pd.DataFrame:
    """
    Retrieve data from the BOReport dataset.

    This function loads data from the Excel file specified in the environment
    variables using the BOReport class from the datasets module.

    Returns:
        pd.DataFrame: The data from the BO report as a pandas DataFrame.

    Raises:
        FileNotFoundError: If the specified Excel file cannot be found.
        Exception: If there's an error reading the Excel file.
    """
    bo_report = BOReport()
    return bo_report.get_data()


def insert_data(
    data: pd.DataFrame,
    database_name: str = "deep-diver-v2",
    collection_name: str = "boreport",
    host: Optional[str] = None,
    port: Optional[int] = None,
) -> int:
    """
    Insert data into MongoDB collection with option to delete existing data.

    Args:
        data: Pandas DataFrame containing the data to insert
        database_name: Name of the database to connect to
        collection_name: Name of the collection to use
        host: MongoDB host address (default: localhost)
        port: MongoDB port (default: 27017)

    Returns:
        int: Number of documents inserted

    Raises:
        ConnectionError: If connection to MongoDB fails
    """
    # Ask user if they want to delete existing data
    user_response = (
        input(
            f"Do you want to delete all existing data in the '{collection_name}' collection? (y/n): "
        )
        .strip()
        .lower()
    )

    with MongoDBClient(
        database_name=database_name,
        collection_name=collection_name,
        host=host,
        port=port,
    ) as client:
        # If user wants to delete data, drop the collection
        if user_response == "y":
            print(f"Dropping collection '{collection_name}'...")
            client.db.drop_collection(collection_name)
            # Recreate the collection
            client.collection = client.db[collection_name]
            print(f"Collection '{collection_name}' dropped and recreated.")

        # Convert DataFrame to list of dictionaries for MongoDB insertion
        records = data.to_dict("records")

        # Insert data
        print(f"Inserting {len(records)} documents into '{collection_name}'...")
        result = client.collection.insert_many(records)

        inserted_count = len(result.inserted_ids)
        print(f"Successfully inserted {inserted_count} documents.")
        return inserted_count


if __name__ == "__main__":
    try:
        # Set up argument parser
        parser = argparse.ArgumentParser(description="Insert data into MongoDB")
        parser.add_argument(
            "--database", default="deep-diver-v2", help="MongoDB database name"
        )
        parser.add_argument(
            "--collection", default="boreport", help="MongoDB collection name"
        )
        args = parser.parse_args()

        # Get data from BOReport
        print("Loading data from BO Report...")
        data = get_boreport_data()
        print(f"Loaded {len(data)} rows of data.")

        # Insert data into MongoDB using the specified database and collection
        insert_data(data, args.database, args.collection)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
